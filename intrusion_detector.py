import cv2
import numpy as np
from datetime import datetime
import os
import time
from config import (
    TELEGRAM_BOT_TOKEN, 
    TELEGRAM_CHAT_ID, 
    LOG_FILE, 
    CAMERA_INDEX, 
    MOTION_THRESHOLD, 
    CONTOUR_MIN_AREA, 
    ALERT_IMAGES_DIR
)
from telegram_handler import TelegramHandler
from logger import IntrusionLogger

class IntrusionDetector:
    def __init__(self):
        self.cap = None
        self.background = None
        self.telegram = TelegramHandler(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.logger = IntrusionLogger(LOG_FILE)
        self.last_alert_time = 0
        self.alert_cooldown = 30  # 30 giây giữa các cảnh báo
        
        # Khởi tạo camera
        self.init_camera()
        
        # Load YOLO để phân biệt người và vật (optional)
        self.init_person_detection()
    
    def init_camera(self):
        """Khởi tạo camera"""
        try:
            self.cap = cv2.VideoCapture(CAMERA_INDEX)
            if not self.cap.isOpened():
                raise Exception("Không thể mở camera")
            
            # Thiết lập độ phân giải
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            print("Camera đã được khởi tạo thành công")
            
        except Exception as e:
            print(f"Lỗi khởi tạo camera: {e}")
            raise
    
    def init_person_detection(self):
        """Khởi tạo YOLO để phát hiện người (optional)"""
        try:
            # Đường dẫn đến các file YOLO (cần tải về)
            self.yolo_net = None
            self.yolo_classes = None
            print("YOLO person detection không được cấu hình")
        except:
            self.yolo_net = None
            print("YOLO không khả dụng, sử dụng motion detection đơn giản")
    
    def detect_motion(self, frame):
        """Phát hiện chuyển động trong frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Khởi tạo background nếu chưa có
        if self.background is None:
            self.background = gray
            return False, None
        
        # Tính toán sự khác biệt
        frame_delta = cv2.absdiff(self.background, gray)
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Tìm contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        motion_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < CONTOUR_MIN_AREA:
                continue
                
            motion_detected = True
            motion_area += area
            
            # Vẽ bounding box
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cập nhật background
        self.background = cv2.addWeighted(self.background, 0.95, gray, 0.05, 0)
        
        return motion_detected and motion_area > MOTION_THRESHOLD, motion_area
    
    def save_alert_image(self, frame):
        """Lưu ảnh khi phát hiện xâm nhập"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alert_{timestamp}.jpg"
        filepath = os.path.join(ALERT_IMAGES_DIR, filename)
        
        cv2.imwrite(filepath, frame)
        return filepath
    
    def process_detection(self, frame, motion_area):
        """Xử lý khi phát hiện xâm nhập"""
        current_time = time.time()
        
        # Kiểm tra cooldown
        if current_time - self.last_alert_time < self.alert_cooldown:
            return
        
        # Lưu ảnh
        image_path = self.save_alert_image(frame)
        
        # Gửi cảnh báo
        detection_type = f"Phát hiện chuyển động (Diện tích: {motion_area})"
        alert_sent = self.telegram.send_alert(detection_type, image_path)
        
        # Ghi log
        self.logger.log_detection(
            detection_type=detection_type,
            confidence=min(motion_area / 10000, 1.0),
            image_path=image_path,
            alert_sent=alert_sent
        )
        
        self.last_alert_time = current_time
        print(f"🚨 Cảnh báo đã được gửi: {detection_type}")
    
    def run(self):
        """Chạy hệ thống giám sát"""
        print("🔍 Bắt đầu giám sát xâm nhập...")
        print("Nhấn 'q' để thoát, 's' để chụp ảnh thủ công")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Không thể đọc frame từ camera")
                    break
                
                # Phát hiện chuyển động
                motion_detected, motion_area = self.detect_motion(frame)
                
                # Xử lý phát hiện
                if motion_detected:
                    self.process_detection(frame, motion_area)
                
                # Hiển thị frame
                cv2.putText(frame, f"Status: {'MOTION DETECTED' if motion_detected else 'MONITORING'}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                           (0, 0, 255) if motion_detected else (0, 255, 0), 2)
                
                cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                           (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.imshow('Intrusion Warning System', frame)
                
                # Xử lý phím bấm
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Chụp ảnh thủ công
                    manual_image = self.save_alert_image(frame)
                    print(f"Đã lưu ảnh thủ công: {manual_image}")
                elif key == ord('r'):
                    # Reset background
                    self.background = None
                    print("Đã reset background")
                    
        except KeyboardInterrupt:
            print("\n🛑 Dừng hệ thống giám sát")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Đã dọn dẹp tài nguyên")

# Test connection
def test_telegram_connection():
    """Test kết nối Telegram"""
    telegram = TelegramHandler(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Gửi tin nhắn test trực tiếp (như trong demo.py)
    success = telegram.send_message("🔧 Test kết nối hệ thống Intrusion Warning")
    
    if success:
        print("✅ Kết nối Telegram thành công")
    else:
        print("❌ Lỗi kết nối Telegram")
    
    return success
