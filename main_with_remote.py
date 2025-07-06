"""
Main file with Remote Control Integration - FIXED VERSION
Intrusion Warning System với điều khiển từ xa qua Telegram
"""

import cv2
import asyncio
import threading
import time
from datetime import datetime
from intrusion_detector import IntrusionDetector
from telegram_handler import TelegramHandler
from logger import IntrusionLogger
from remote_control import start_remote_bot, remote_controller
from config import CAMERA_INDEX, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class IntrusionSystemWithRemote:
    def __init__(self):
        self.detector = IntrusionDetector()
        self.telegram = TelegramHandler(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.logger = IntrusionLogger("intrusion_log.csv")
        self.running = False
        self.remote_bot = None
        self.bot_thread = None
        
    def start_remote_bot_thread(self):
        """Khởi động bot Telegram trong thread riêng"""
        try:
            self.remote_bot = start_remote_bot()
            if self.remote_bot:
                # Chạy bot trong event loop riêng
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                print("🤖 Bot điều khiển từ xa đã sẵn sàng!")
                print("📱 Các lệnh Telegram:")
                print("   /chup - Chụp ảnh")
                print("   /mo - Bật camera")
                print("   /thoat - Tắt camera")
                
                self.remote_bot.run_polling()
            else:
                print("❌ Không thể khởi động bot điều khiển từ xa")
        except Exception as e:
            print(f"❌ Lỗi bot: {e}")
    
    def start(self):
        """Khởi động hệ thống với remote control"""
        print("🚀 Đang khởi động Hệ thống Cảnh báo Xâm nhập...")
        
        # Test Telegram trước
        print("📱 Đang test kết nối Telegram...")
        if self.telegram.send_message("🔄 Hệ thống cảnh báo xâm nhập đã khởi động"):
            print("✅ Telegram hoạt động tốt")
        else:
            print("❌ Telegram có vấn đề, kiểm tra config")
            return
        
        # Khởi động bot điều khiển từ xa trong thread riêng
        self.bot_thread = threading.Thread(target=self.start_remote_bot_thread)
        self.bot_thread.daemon = True
        self.bot_thread.start()
        
        # Khởi tạo camera
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            print("❌ Không thể mở camera")
            return
        
        # Chia sẻ camera với remote controller
        remote_controller.set_shared_camera(cap)
        
        print("📹 Camera đã sẵn sàng")
        print("\n🎮 Điều khiển:")
        print("  [q] - Thoát")
        print("  [s] - Chụp ảnh thủ công")
        print("  [r] - Reset/học lại ảnh nền")
        print("  [m] - Test phát hiện chuyển động")
        print("\n📱 Remote Telegram:")
        print("  /chup - Chụp ảnh từ xa (KHÔNG tắt chương trình)")
        print("  /mo - Bật camera giám sát")
        print("  /thoat - Tắt camera giám sát")
        print("\n⚡ Hệ thống đang hoạt động...\n")
        
        self.running = True
        frame_count = 0
        
        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Không thể đọc frame từ camera")
                    break
                
                # Cập nhật frame cho remote controller để chụp ảnh nhanh
                remote_controller.update_frame(frame)
                
                frame_count += 1
                
                # Xử lý phát hiện (mỗi 5 frame để giảm lag)
                if frame_count % 5 == 0:
                    # Tạo bản copy để phát hiện (không có box)
                    detection_frame = frame.copy()
                    motion_detected, area = self.detector.detect_motion(detection_frame, draw_boxes=False)
                    
                    if motion_detected and area > 5000:  # Chỉ gửi cảnh báo nếu > 5000 pixels
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        print(f"🚨 Phát hiện xâm nhập! Diện tích: {area:.1f} pixels")
                          
                        # Gửi cảnh báo Telegram
                        message = f"🚨 CẢNH BÁO XÂM NHẬP!\n📅 Thời gian: {timestamp}\n📏 Diện tích: {area:.1f} pixels"
                        
                        # Lưu ảnh GỐCKCK (không có box xanh) để gửi Telegram
                        filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"alert_{filename_timestamp}.jpg"
                        filepath = f"alert_images/{filename}"
                        cv2.imwrite(filepath, frame)  # Lưu frame gốc, không có box
                        print(f"💾 Đã lưu ảnh: {filepath}")
                        
                        # Gửi tin nhắn và ảnh
                        if self.telegram.send_message(message):
                            print("✅ Đã gửi cảnh báo Telegram")
                            if self.telegram.send_photo(filepath, "🚨 Ảnh cảnh báo xâm nhập"):
                                print("✅ Đã gửi ảnh qua Telegram")
                            else:
                                print("❌ Lỗi gửi ảnh qua Telegram")
                        else:
                            print("❌ Lỗi gửi tin nhắn Telegram")
                        
                        # Ghi log
                        try:
                            self.logger.log_intrusion(timestamp, area, filename)
                            print(f"📝 Đã ghi log: {timestamp} - Diện tích: {area:.1f}")
                        except Exception as e:
                            print(f"❌ Lỗi ghi log: {e}")
                    elif motion_detected:
                        # Hiển thị thông tin nhưng không gửi cảnh báo
                        print(f"👁️ Phát hiện chuyển động nhỏ: {area:.1f} pixels (< 5000, không gửi cảnh báo)")
                
                # Hiển thị frame với overlay và box phát hiện (mỗi 5 frame để giảm lag)
                if frame_count % 5 == 0:
                    display_frame = frame.copy()
                    
                    # Chạy detect với box để hiển thị trên màn hình
                    self.detector.detect_motion(display_frame, draw_boxes=True)
                    
                    # Thêm thông tin trạng thái
                    status_text = "GIAM SAT" if self.running else "DUNG"
                    cv2.putText(display_frame, status_text, (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    # Thêm ngưỡng phát hiện
                    threshold_text = "Nguong: >5000px"
                    cv2.putText(display_frame, threshold_text, (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    
                    cv2.imshow("Intrusion Warning", display_frame)
                
                # Xử lý phím
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("👋 Đang thoát...")
                    break
                elif key == ord('s'):
                    # Chụp ảnh thủ công
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"manual_{timestamp}.jpg"
                    filepath = f"alert_images/{filename}"
                    cv2.imwrite(filepath, frame)
                    print(f"📸 Đã chụp ảnh: {filepath}")
                    if self.telegram.send_photo(filepath, "📸 Ảnh chụp thủ công"):
                        print("✅ Đã gửi ảnh thủ công qua Telegram")
                    else:
                        print("❌ Lỗi gửi ảnh thủ công")
                elif key == ord('r'):
                    # Reset ảnh nền
                    self.detector.reset_background()
                    print("🔄 Đã reset ảnh nền")
                elif key == ord('m'):
                    # Test phát hiện chuyển động thủ công
                    print("🧪 TEST: Giả lập phát hiện chuyển động")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    test_area = 8500.0
                    
                    # Lưu ảnh test
                    filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"test_{filename_timestamp}.jpg"
                    filepath = f"alert_images/{filename}"
                    cv2.imwrite(filepath, frame)
                    
                    # Gửi cảnh báo test
                    message = f"🧪 TEST CẢNH BÁO!\n📅 Thời gian: {timestamp}\n📏 Diện tích: {test_area} pixels"
                    if self.telegram.send_message(message):
                        print("✅ Đã gửi tin nhắn test")
                        if self.telegram.send_photo(filepath, "🧪 Ảnh test cảnh báo"):
                            print("✅ Đã gửi ảnh test")
                        else:
                            print("❌ Lỗi gửi ảnh test")
                    else:
                        print("❌ Lỗi gửi tin nhắn test")
                    
                    # Ghi log test
                    try:
                        self.logger.log_intrusion(timestamp, test_area, filename)
                        print(f"📝 Đã ghi log test: {timestamp}")
                    except Exception as e:
                        print(f"❌ Lỗi ghi log test: {e}")
                
                time.sleep(0.05)  # ~20 FPS (giảm từ 30 FPS để tiết kiệm tài nguyên)
                
        except KeyboardInterrupt:
            print("\n⚠️ Nhận Ctrl+C, đang thoát...")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            print(f"❌ System error: {str(e)}")
        finally:
            self.cleanup(cap)
    
    def cleanup(self, cap):
        """Dọn dẹp tài nguyên"""
        self.running = False
        
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        
        # Gửi thông báo tắt hệ thống
        try:
            self.telegram.send_message("⭕ Hệ thống cảnh báo đã tắt")
        except:
            pass
        
        print("🔄 Đã dọn dẹp tài nguyên")
        print("👋 Tạm biệt!")

if __name__ == "__main__":
    system = IntrusionSystemWithRemote()
    system.start()
