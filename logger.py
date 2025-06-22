import csv
import os
import logging
from datetime import datetime

class IntrusionLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.setup_logging()
        self.init_csv()
    
    def setup_logging(self):
        """Thiết lập logging cho hệ thống"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system.log', encoding='utf-8'),
                logging.StreamHandler()
            ],
            force=True
        )
    
    def init_csv(self):
        """Khởi tạo file CSV với header nếu chưa tồn tại"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 
                    'Detection_Type',                    'Confidence', 
                    'Image_Path', 
                    'Alert_Sent'
                ])
    
    def log_detection(self, detection_type, confidence=0, image_path="", alert_sent=False):
        """Ghi log phát hiện xâm nhập"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                detection_type,
                confidence,
                image_path,
                alert_sent
            ])
        
        # Sử dụng ASCII để tránh lỗi encoding
        detection_ascii = detection_type.encode('ascii', 'ignore').decode('ascii')
        logging.info(f"Detection logged: {detection_ascii} at {timestamp}")
    
    def get_detection_history(self, limit=10):
        """Lấy lịch sử phát hiện gần nhất"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                records = list(reader)
                return records[-limit:] if len(records) > limit else records
        except Exception as e:
            logging.error(f"Error reading detection history: {e}")
            return []
