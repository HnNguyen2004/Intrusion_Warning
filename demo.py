"""
Demo script để test các chức năng của hệ thống Intrusion Warning
"""

from config import (
    TELEGRAM_BOT_TOKEN, 
    TELEGRAM_CHAT_ID, 
    LOG_FILE, 
    CAMERA_INDEX, 
    ALERT_IMAGES_DIR
)
from telegram_handler import TelegramHandler
from logger import IntrusionLogger
import cv2
import time

def test_camera():
    """Test camera connection"""
    print("📹 Testing camera connection...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("❌ Camera không thể mở")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print("❌ Không thể đọc frame từ camera")
        cap.release()
        return False
    
    print(f"✅ Camera hoạt động bình thường (Resolution: {frame.shape[1]}x{frame.shape[0]})")
    cap.release()
    return True

def test_telegram():
    """Test Telegram connection"""
    print("📱 Testing Telegram connection...")
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  Telegram Bot Token chưa được cấu hình")
        return False
    
    telegram = TelegramHandler(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    success = telegram.send_message("🧪 Test message từ Intrusion Warning System")
    
    if success:
        print("✅ Telegram connection thành công")
    else:
        print("❌ Telegram connection thất bại")
    
    return success

def test_logger():
    """Test logging system"""
    print("📝 Testing logger...")
    
    logger = IntrusionLogger(LOG_FILE)
    logger.log_detection(
        detection_type="Test Detection",
        confidence=0.95,
        image_path="test_image.jpg",
        alert_sent=True
    )
    
    # Đọc lại log
    history = logger.get_detection_history(1)
    if history and len(history) > 0:
        print("✅ Logger hoạt động bình thường")
        print(f"   Last log: {history[-1]}")
        return True
    else:
        print("❌ Logger không hoạt động")
        return False

def test_directories():
    """Test thư mục và file"""
    print("📁 Testing directories...")
    
    import os
    
    # Kiểm tra thư mục alert_images
    if os.path.exists(ALERT_IMAGES_DIR):
        print(f"✅ Thư mục {ALERT_IMAGES_DIR} tồn tại")
    else:
        print(f"❌ Thư mục {ALERT_IMAGES_DIR} không tồn tại")
        return False
    
    # Thử tạo file test trong thư mục
    test_file = os.path.join(ALERT_IMAGES_DIR, "test.txt")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"✅ Có thể ghi file vào {ALERT_IMAGES_DIR}")
    except Exception as e:
        print(f"❌ Không thể ghi file: {e}")
        return False
    
    return True

def main():
    """Chạy tất cả các test"""
    print("=" * 60)
    print("🧪 INTRUSION WARNING SYSTEM - DEMO & TEST")
    print("=" * 60)
    
    tests = [
        ("Directories", test_directories),
        ("Camera", test_camera),
        ("Logger", test_logger),
        ("Telegram", test_telegram),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n[{test_name.upper()}]")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Lỗi trong test {test_name}: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Delay giữa các test
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("📋 KẾT QUẢ TEST:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} : {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Tổng kết: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Tất cả test đều PASS! Hệ thống sẵn sàng hoạt động.")
        print("\nChạy lệnh sau để bắt đầu giám sát:")
        print("python main.py")
    else:
        print("⚠️  Một số test FAIL. Hãy kiểm tra cấu hình trước khi chạy hệ thống.")
        
        if not any(name == "Telegram" and result for name, result in results):
            print("\n💡 Hướng dẫn cấu hình Telegram:")
            print("1. Tạo bot tại @BotFather")
            print("2. Lấy Bot Token")
            print("3. Lấy Chat ID")
            print("4. Cập nhật config.py")

if __name__ == "__main__":
    main()
