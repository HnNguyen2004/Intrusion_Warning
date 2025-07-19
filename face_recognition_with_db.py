import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import logging
from database_config import DatabaseManager
# Import telegram code hiện tại của bạn
# from telegram_sender import send_telegram_alert

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceRecognitionWithDB:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.db_manager = DatabaseManager()
        self.db_connected = False
        
        # Kết nối database
        if self.db_manager.connect():
            self.db_connected = True
            logging.info("Connected to database successfully")
        else:
            logging.error("Failed to connect to database")
    
    def load_known_faces(self, faces_directory="known_faces"):
        # ...existing code for loading faces...
        pass
    
    def save_intrusion_image(self, frame, person_name):
        """Lưu ảnh người xâm nhập"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intrusion_{person_name}_{timestamp}.jpg"
        
        # Tạo thư mục nếu chưa có
        os.makedirs("intrusion_images", exist_ok=True)
        
        image_path = os.path.join("intrusion_images", filename)
        cv2.imwrite(image_path, frame)
        
        return image_path
    
    def process_intrusion(self, frame, person_name, confidence, location="Camera_01"):
        """Xử lý khi phát hiện người xâm nhập"""
        # Lưu ảnh
        image_path = self.save_intrusion_image(frame, person_name)
        
        log_id = None
        telegram_sent = False
        
        # Lưu vào database
        if self.db_connected:
            log_id = self.db_manager.insert_intrusion_log(
                person_name=person_name,
                confidence=confidence,
                image_path=image_path,
                location=location,
                telegram_sent=False,
                notes=f"Detected via {location}"
            )
        
        # Gửi telegram (sử dụng code hiện tại của bạn)
        try:
            # send_telegram_alert(person_name, confidence, image_path)
            telegram_sent = True
            logging.info(f"Telegram alert sent for {person_name}")
            
            # Cập nhật trạng thái telegram trong database
            if self.db_connected and log_id:
                self.db_manager.update_telegram_status(log_id, True)
                
        except Exception as e:
            logging.error(f"Failed to send telegram: {e}")
        
        return log_id, telegram_sent
    
    def recognize_faces(self, frame):
        """Nhận dạng khuôn mặt trong frame"""
        # ...existing face recognition code...
        
        # Khi phát hiện người lạ hoặc người xâm nhập:
        # unknown_person hoặc intruder_detected = True
        # confidence = calculated_confidence
        # person_name = "Unknown" hoặc tên người
        
        # Gọi process_intrusion
        # self.process_intrusion(frame, person_name, confidence)
        
        pass
    
    def get_recent_intrusions(self, limit=10):
        """Lấy danh sách xâm nhập gần đây"""
        if self.db_connected:
            return self.db_manager.get_recent_logs(limit)
        return []
    
    def cleanup(self):
        """Dọn dẹp kết nối"""
        if self.db_connected:
            self.db_manager.disconnect()

# Ví dụ sử dụng
if __name__ == "__main__":
    recognizer = FaceRecognitionWithDB()
    
    # Load các khuôn mặt đã biết
    recognizer.load_known_faces()
    
    # Khởi động camera và nhận dạng
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if ret:
                recognizer.recognize_faces(frame)
                
                # Hiển thị frame
                cv2.imshow('Intrusion Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        recognizer.cleanup()
