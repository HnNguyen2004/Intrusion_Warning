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
        
        # Thông số điều chỉnh ngưỡng
        self.current_threshold = 5000  # Ngưỡng hiện tại
        self.current_motion_area = 0   # Diện tích chuyển động hiện tại
        self.threshold_step = 500      # Bước tăng/giảm ngưỡng
        
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
    
    def draw_ui_overlay(self, frame):
        """Vẽ overlay UI một cách tối ưu"""
        # Thông tin trạng thái
        status_text = "GIAM SAT" if self.running else "DUNG"
        status_color = (0, 255, 0) if self.running else (0, 0, 255)
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Ngưỡng hiện tại
        threshold_text = f"Nguong: {self.current_threshold}px"
        cv2.putText(frame, threshold_text, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Diện tích chuyển động
        area_text = f"Dien tich: {self.current_motion_area:.0f}px"
        area_color = (0, 0, 255) if self.current_motion_area > self.current_threshold else (255, 255, 255)
        cv2.putText(frame, area_text, (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, area_color, 2)
        
        # Progress bar tối ưu
        self.draw_progress_bar(frame)
        
        # Hướng dẫn (chỉ vẽ khi cần)
        cv2.putText(frame, "+/-: Nguong  0: Reset", (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    def draw_progress_bar(self, frame):
        """Vẽ progress bar tối ưu"""
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 110
        
        # Vẽ khung
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), 2)
        
        # Tính tỷ lệ một lần
        max_val = 50000.0
        threshold_width = int(bar_width * min(self.current_threshold / max_val, 1.0))
        area_width = int(bar_width * min(self.current_motion_area / max_val, 1.0))
        
        # Vẽ thanh ngưỡng (vàng)
        if threshold_width > 0:
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + threshold_width, bar_y + bar_height), (0, 255, 255), -1)
        
        # Vẽ thanh diện tích hiện tại
        if area_width > 0:
            color = (0, 0, 255) if self.current_motion_area > self.current_threshold else (255, 255, 255)
            cv2.rectangle(frame, (bar_x, bar_y + 5), (bar_x + area_width, bar_y + 15), color, -1)
    
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
        print("  [+] hoặc [=] - Tăng ngưỡng phát hiện (+500)")
        print("  [-] - Giảm ngưỡng phát hiện (-500)")
        print("  [0] - Reset ngưỡng về 5000")
        print("\n📱 Remote Telegram:")
        print("  /chup - Chụp ảnh từ xa (KHÔNG tắt chương trình)")
        print("  /mo - Bật camera giám sát")
        print("  /thoat - Tắt camera giám sát")
        print(f"\n⚡ Hệ thống đang hoạt động... (Ngưỡng hiện tại: {self.current_threshold} pixels)\n")
        
        self.running = True
        frame_count = 0
        last_detection_time = 0
        last_display_update = 0
        
        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Không thể đọc frame từ camera")
                    break
                
                # Cập nhật frame cho remote controller (luôn luôn để đảm bảo chụp ảnh real-time)
                remote_controller.update_frame(frame)
                
                frame_count += 1
                current_time = time.time()
                
                # Xử lý phát hiện chỉ mỗi 10 frame (thay vì 5) để tăng FPS
                if frame_count % 10 == 0:
                    # Tạo bản copy để phát hiện (không có box)
                    detection_frame = frame.copy()
                    motion_detected, area = self.detector.detect_motion(detection_frame, draw_boxes=False)
                    
                    # Cập nhật diện tích chuyển động hiện tại
                    self.current_motion_area = area
                    last_detection_time = current_time
                    
                    if motion_detected and area > self.current_threshold:  # Sử dụng ngưỡng có thể điều chỉnh
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        print(f"🚨 Phát hiện xâm nhập! Diện tích: {area:.1f} pixels (Ngưỡng: {self.current_threshold})")
                          
                        # Gửi cảnh báo Telegram
                        message = f"🚨 CẢNH BÁO XÂM NHẬP!\n📅 Thời gian: {timestamp}\n📏 Diện tích: {area:.1f} pixels\n🎯 Ngưỡng: {self.current_threshold} pixels"
                        
                        # Lưu ảnh GỐC (không có box xanh) để gửi Telegram
                        filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"alert_{filename_timestamp}.jpg"
                        filepath = f"alert_images/{filename}"
                        cv2.imwrite(filepath, frame)  # Lưu frame gốc, không có box
                        print(f"💾 Đã lưu ảnh: {filepath}")
                        
                        # Gửi tin nhắn và ảnh (trong thread riêng để không block)
                        def send_telegram_alert():
                            if self.telegram.send_message(message):
                                print("✅ Đã gửi cảnh báo Telegram")
                                if self.telegram.send_photo(filepath, "🚨 Ảnh cảnh báo xâm nhập"):
                                    print("✅ Đã gửi ảnh qua Telegram")
                                else:
                                    print("❌ Lỗi gửi ảnh qua Telegram")
                            else:
                                print("❌ Lỗi gửi tin nhắn Telegram")
                        
                        # Chạy Telegram trong thread riêng để không làm chậm FPS
                        telegram_thread = threading.Thread(target=send_telegram_alert)
                        telegram_thread.daemon = True
                        telegram_thread.start()
                        
                        # Ghi log
                        try:
                            self.logger.log_intrusion(timestamp, area, filename)
                            print(f"📝 Đã ghi log: {timestamp} - Diện tích: {area:.1f}")
                        except Exception as e:
                            print(f"❌ Lỗi ghi log: {e}")
                    elif motion_detected:
                        # Hiển thị thông tin nhưng không gửi cảnh báo (chỉ khi debug)
                        if frame_count % 50 == 0:  # Chỉ print mỗi 50 frame để giảm spam
                            print(f"👁️ Phát hiện chuyển động nhỏ: {area:.1f} pixels (< {self.current_threshold}, không gửi cảnh báo)")
                
                # Hiển thị frame - CẢI THIỆN FPS
                # Chỉ cập nhật UI mỗi 3 frame thay vì 5 để mượt hơn
                if frame_count % 3 == 0 or current_time - last_display_update > 0.033:  # Tối đa 30 FPS display
                    display_frame = frame.copy()
                    
                    # Chỉ chạy detect với box khi thực sự cần hiển thị
                    if frame_count % 6 == 0:  # Giảm tần suất vẽ box
                        self.detector.detect_motion(display_frame, draw_boxes=True)
                    
                    # Tối ưu hiển thị text - ít phép tính hơn
                    self.draw_ui_overlay(display_frame)
                    
                    cv2.imshow("Intrusion Warning", display_frame)
                    last_display_update = current_time
                
                # Xử lý phím - tối ưu
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # Chỉ xử lý khi có phím được nhấn
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
                        
                        # Gửi Telegram trong thread riêng
                        def send_manual_photo():
                            if self.telegram.send_photo(filepath, "📸 Ảnh chụp thủ công"):
                                print("✅ Đã gửi ảnh thủ công qua Telegram")
                            else:
                                print("❌ Lỗi gửi ảnh thủ công")
                        
                        threading.Thread(target=send_manual_photo, daemon=True).start()
                        
                    elif key == ord('r'):
                        # Reset ảnh nền
                        self.detector.reset_background()
                        print("🔄 Đã reset ảnh nền")
                    elif key == ord('+') or key == ord('='):
                        # Tăng ngưỡng
                        self.current_threshold += self.threshold_step
                        print(f"📈 Tăng ngưỡng lên: {self.current_threshold} pixels")
                    elif key == ord('-'):
                        # Giảm ngưỡng (không cho phép âm)
                        self.current_threshold = max(500, self.current_threshold - self.threshold_step)
                        print(f"📉 Giảm ngưỡng xuống: {self.current_threshold} pixels")
                    elif key == ord('0'):
                        # Reset ngưỡng về mặc định
                        self.current_threshold = 5000
                        print(f"🔄 Reset ngưỡng về: {self.current_threshold} pixels")
                    elif key == ord('m'):
                        # Test phát hiện chuyển động thủ công
                        print("🧪 TEST: Giả lập phát hiện chuyển động")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        test_area = self.current_threshold + 500
                        
                        # Lưu ảnh test
                        filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"test_{filename_timestamp}.jpg"
                        filepath = f"alert_images/{filename}"
                        cv2.imwrite(filepath, frame)
                        
                        # Gửi test trong thread riêng
                        def send_test_alert():
                            message = f"🧪 TEST CẢNH BÁO!\n📅 Thời gian: {timestamp}\n📏 Diện tích: {test_area} pixels\n🎯 Ngưỡng: {self.current_threshold} pixels"
                            if self.telegram.send_message(message):
                                print("✅ Đã gửi tin nhắn test")
                                if self.telegram.send_photo(filepath, "🧪 Ảnh test cảnh báo"):
                                    print("✅ Đã gửi ảnh test")
                                else:
                                    print("❌ Lỗi gửi ảnh test")
                            else:
                                print("❌ Lỗi gửi tin nhắn test")
                        
                        threading.Thread(target=send_test_alert, daemon=True).start()
                        
                        # Ghi log test
                        try:
                            self.logger.log_intrusion(timestamp, test_area, filename)
                            print(f"📝 Đã ghi log test: {timestamp}")
                        except Exception as e:
                            print(f"❌ Lỗi ghi log test: {e}")
                
                # Giảm sleep time để tăng FPS
                time.sleep(0.01)  # ~60 FPS potential (thay vì 0.05 = 20 FPS)
                
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
