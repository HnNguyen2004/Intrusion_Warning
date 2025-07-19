import cv2
import numpy as np
from main import IntrusionDetectionSystem

def test_intrusion_logging():
    """Test việc lưu intrusion vào database"""
    system = IntrusionDetectionSystem()
    
    # Tạo frame test
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(test_frame, "TEST INTRUSION", (50, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Test lưu database
    print("Testing database logging...")
    log_id, image_path = system.log_intrusion_to_database(
        test_frame, 
        "Test_Person", 
        0.95, 
        "Test_Camera"
    )
    
    if log_id:
        print(f"✓ Successfully logged intrusion with ID: {log_id}")
        print(f"✓ Image saved at: {image_path}")
        
        # Test update telegram status
        system.update_telegram_status_in_db(log_id, True)
        print("✓ Telegram status updated")
    else:
        print("✗ Failed to log intrusion")
    
    system.cleanup()

if __name__ == "__main__":
    test_intrusion_logging()
