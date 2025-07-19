from database_config import DatabaseManager
import cv2
import numpy as np
from datetime import datetime

def test_database_integration():
    """Test việc lưu thông tin vào database"""
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("✗ Cannot connect to database")
        return
    
    print("✓ Database connected")
    
    # Tạo ảnh test
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(test_image, "TEST INTRUSION", (50, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Lưu ảnh test
    image_path = f"test_intrusion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(image_path, test_image)
    
    # Lưu vào database
    log_id = db_manager.insert_intrusion_log(
        person_name="Test_Person",
        confidence=0.85,
        image_path=image_path,
        location="Test_Camera",
        telegram_sent=False,
        notes="This is a test entry"
    )
    
    if log_id:
        print(f"✓ Test record inserted with ID: {log_id}")
        
        # Test cập nhật telegram status
        if db_manager.update_telegram_status(log_id, True):
            print("✓ Telegram status updated")
        
        # Test lấy logs
        logs = db_manager.get_recent_logs(5)
        print(f"✓ Retrieved {len(logs)} recent logs")
        
        if logs:
            latest_log = logs[0]
            print(f"Latest log: {latest_log['person_name']} at {latest_log['timestamp']}")
    
    db_manager.disconnect()
    print("✓ Test completed")

if __name__ == "__main__":
    test_database_integration()
