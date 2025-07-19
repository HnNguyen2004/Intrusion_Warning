import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect
from database_config import DatabaseManager
import os
from datetime import datetime

class IntrusionDetectionSystem:
    def __init__(self):
        self.video = VideoStream(src=0).start()
        self.points = []
        self.model = YoloDetect()
        self.detect = False

        # Thêm database manager
        self.db_manager = DatabaseManager()
        self.db_connected = False
        
        # Kết nối database
        if self.db_manager.connect():
            self.db_connected = True
            print("✓ Database connected successfully")
        else:
            print("✗ Failed to connect to database")
        
        self.last_detection_time = 0
        self.detection_cooldown = 5  # 5 giây giữa các lần lưu
        
        # Đặt callback cho YoloDetect
        self.model.set_intrusion_callback(self.on_intrusion_detected)

    def handle_left_click(self, event, x, y, flags, points):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y])

    def draw_polygon(self, frame, points):
        for point in points:
            frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)
        if len(points) > 1:
            frame = cv2.polylines(frame, [np.int32(points)], False, (255, 0, 0), thickness=2)
        return frame

    def save_intrusion_image(self, frame, person_name="Unknown"):
        """Lưu ảnh người xâm nhập"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intrusion_{person_name}_{timestamp}.jpg"
        
        # Tạo thư mục nếu chưa có
        os.makedirs("intrusion_images", exist_ok=True)
        
        image_path = os.path.join("intrusion_images", filename)
        cv2.imwrite(image_path, frame)
        
        return image_path
    
    def log_intrusion_to_database(self, frame, person_name="Unknown", confidence=0.0, location="Camera_01"):
        """Lưu thông tin xâm nhập vào database"""
        log_id = None
        image_path = None
        
        try:
            # Lưu ảnh
            image_path = self.save_intrusion_image(frame, person_name)
            
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
                print(f"✓ Intrusion logged to database with ID: {log_id}")
            
            return log_id, image_path
            
        except Exception as e:
            print(f"✗ Error logging intrusion: {e}")
            return None, image_path
    
    def update_telegram_status_in_db(self, log_id, success=True):
        """Cập nhật trạng thái gửi telegram trong database"""
        if self.db_connected and log_id:
            try:
                self.db_manager.update_telegram_status(log_id, success)
                print(f"✓ Telegram status updated for log ID: {log_id}")
            except Exception as e:
                print(f"✗ Error updating telegram status: {e}")

    def on_intrusion_detected(self, frame, person_name="Person_Detected", confidence=0.8):
        """Callback được gọi khi YoloDetect phát hiện xâm nhập"""
        current_time = datetime.now().timestamp()
        
        # Kiểm tra cooldown để tránh spam
        if (current_time - self.last_detection_time) > self.detection_cooldown:
            print(f"🚨 Intrusion detected: {person_name} (confidence: {confidence})")
            
            # Lưu vào database
            log_id, image_path = self.log_intrusion_to_database(
                frame, 
                person_name, 
                confidence, 
                "Camera_01"
            )
            
            # Cập nhật thời gian detection
            self.last_detection_time = current_time
            
            # Cập nhật trạng thái telegram (giả sử telegram đã được gửi thành công trong yolodetect.py)
            if log_id:
                self.update_telegram_status_in_db(log_id, True)

    def run(self):
        cv2.namedWindow("Intrusion Warning")
        cv2.setMouseCallback("Intrusion Warning", self.handle_left_click, self.points)

        while True:
            frame = self.video.read()
            frame = cv2.flip(frame, 1)

            frame = self.draw_polygon(frame, self.points)

            if self.detect:
                # Detect với YOLO (callback sẽ được gọi tự động từ yolodetect.py)
                frame = self.model.detect(frame=frame, points=self.points)

            cv2.imshow("Intrusion Warning", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('d'):
                if len(self.points) > 2:
                    self.points.append(self.points[0])
                    self.detect = True

    def cleanup(self):
        """Dọn dẹp khi thoát"""
        self.video.stop()
        cv2.destroyAllWindows()
        
        # Đóng kết nối database
        if self.db_connected:
            self.db_manager.disconnect()
            print("✓ Database connection closed")

if __name__ == "__main__":
    system = IntrusionDetectionSystem()
    
    try:
        system.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        system.cleanup()
