"""
Remote Control Module for Intrusion Warning System
Handles Telegram bot commands: /chup, /mo, /thoat
"""

import cv2
import os
import threading
import time
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ALERT_IMAGES_DIR

class RemoteController:
    def __init__(self):
        self.shared_camera = None  # Camera sẽ được chia sẻ từ main system
        self.camera_active = False
        self.monitoring_thread = None
        self.should_stop = False
        self.last_frame = None  # Lưu frame cuối cùng để chụp nhanh
        
    def set_shared_camera(self, camera):
        """Thiết lập camera chia sẻ từ main system"""
        self.shared_camera = camera
        
    def update_frame(self, frame):
        """Cập nhật frame mới nhất từ main system"""
        self.last_frame = frame.copy()
        
    def take_photo(self):
        """Chụp ảnh từ camera - KHÔNG tắt chương trình"""
        try:
            # Sử dụng frame hiện tại thay vì tạo camera mới
            if self.last_frame is not None:
                # Lưu ảnh từ frame hiện tại
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"remote_capture_{timestamp}.jpg"
                filepath = os.path.join(ALERT_IMAGES_DIR, filename)
                cv2.imwrite(filepath, self.last_frame)
                
                return filepath, "📸 Chụp ảnh thành công từ camera chính"
            
            # Fallback: nếu không có frame, thử camera trực tiếp NHƯNG KHÔNG giữ lâu
            elif self.shared_camera is not None:
                ret, frame = self.shared_camera.read()
                if ret:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"remote_capture_{timestamp}.jpg"
                    filepath = os.path.join(ALERT_IMAGES_DIR, filename)
                    cv2.imwrite(filepath, frame)
                    
                    return filepath, "📸 Chụp ảnh thành công"
                else:
                    return None, "❌ Không thể đọc frame từ camera"
            else:
                return None, "❌ Camera chưa sẵn sàng"
                
        except Exception as e:
            print(f"Lỗi khi chụp ảnh: {str(e)}")
            return None, f"❌ Lỗi: {str(e)}"
    
    def start_camera_monitoring(self):
        """Bắt đầu giám sát camera"""
        try:
            if self.camera_active:
                return "📹 Camera đã đang hoạt động"
            
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                return "❌ Không thể kết nối camera"
            
            self.camera_active = True
            self.should_stop = False
            
            # Tạo thread riêng để hiển thị camera
            self.monitoring_thread = threading.Thread(target=self._camera_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            print("Camera monitoring started via remote command")
            return "📹 Đã bật camera giám sát. Nhấn 'q' trên cửa sổ camera để tắt."
            
        except Exception as e:
            print(f"Lỗi khi bật camera: {str(e)}")
            return f"❌ Lỗi: {str(e)}"
    
    def _camera_loop(self):
        """Vòng lặp hiển thị camera"""
        cv2.namedWindow("📹 Remote Camera Monitor", cv2.WINDOW_AUTOSIZE)
        
        while self.camera_active and not self.should_stop:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                # Thêm timestamp lên ảnh
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, f"Remote Monitor: {timestamp}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow("📹 Remote Camera Monitor", frame)
                
                # Thoát khi nhấn 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
                time.sleep(0.03)  # ~30 FPS
                
            except Exception as e:
                print(f"Lỗi trong camera loop: {str(e)}")
                break
        
        self._cleanup_camera()
    
    def stop_monitoring(self):
        """Dừng giám sát camera"""
        try:
            if not self.camera_active:
                return "📹 Camera chưa được bật"
            
            self.should_stop = True
            self.camera_active = False
            
            # Đợi thread kết thúc
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=2)
            
            self._cleanup_camera()
            print("Camera monitoring stopped via remote command")
            return "📹 Đã tắt camera giám sát"
            
        except Exception as e:
            print(f"Lỗi khi tắt camera: {str(e)}")
            return f"❌ Lỗi: {str(e)}"
    
    def _cleanup_camera(self):
        """Dọn dẹp camera"""
        if self.camera:
            self.camera.release()
            self.camera = None
        cv2.destroyAllWindows()
        self.camera_active = False

# Khởi tạo controller toàn cục
remote_controller = RemoteController()

# Bot command handlers
async def cmd_chup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /chup - chụp ảnh"""
    # Kiểm tra quyền truy cập
    chat_id = str(update.effective_chat.id)
    if chat_id != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Bạn không có quyền sử dụng bot này")
        return
    
    await update.message.reply_text("📸 Đang chụp ảnh...")
    
    filepath, message = remote_controller.take_photo()
    
    if filepath and os.path.exists(filepath):
        # Gửi ảnh về Telegram
        try:
            with open(filepath, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=message)
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi gửi ảnh: {str(e)}")
    else:
        await update.message.reply_text(message)

async def cmd_mo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /mo - mở camera"""
    # Kiểm tra quyền truy cập
    chat_id = str(update.effective_chat.id)
    if chat_id != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Bạn không có quyền sử dụng bot này")
        return
    
    message = remote_controller.start_camera_monitoring()
    await update.message.reply_text(message)

async def cmd_thoat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /thoat - tắt camera"""
    # Kiểm tra quyền truy cập
    chat_id = str(update.effective_chat.id)
    if chat_id != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Bạn không có quyền sử dụng bot này")
        return
    
    message = remote_controller.stop_monitoring()
    await update.message.reply_text(message)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start - hướng dẫn sử dụng"""
    help_text = """🤖 **Bot Điều Khiển Camera Từ Xa**

📋 **Các lệnh có sẵn:**
• /chup - Chụp ảnh từ camera
• /mo - Bật camera giám sát  
• /thoat - Tắt camera giám sát
• /help - Hiển thị hướng dẫn này

🔒 **Bảo mật:** Chỉ chủ sở hữu mới có thể sử dụng bot này."""
    await update.message.reply_text(help_text)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /help"""
    await cmd_start(update, context)

def start_remote_bot():
    """Khởi động bot điều khiển từ xa"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Chưa cấu hình TELEGRAM_BOT_TOKEN")
        return None
    
    # Tạo application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Thêm handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("chup", cmd_chup))
    app.add_handler(CommandHandler("mo", cmd_mo))
    app.add_handler(CommandHandler("thoat", cmd_thoat))
    
    return app

if __name__ == "__main__":
    # Test chạy bot
    print("🤖 Khởi động Bot Điều Khiển Từ Xa...")
    app = start_remote_bot()
    if app:
        print("✅ Bot đã sẵn sàng! Gửi /start để xem hướng dẫn.")
        app.run_polling()
