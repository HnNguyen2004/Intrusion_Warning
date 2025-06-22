from intrusion_detector import IntrusionDetector, test_telegram_connection
import sys

def main():
    print("=" * 50)
    print("🏠 INTRUSION WARNING SYSTEM")
    print("=" * 50)
    
    # Test kết nối Telegram trước
    print("Đang test kết nối Telegram...")
    if not test_telegram_connection():
        print("⚠️  Cảnh báo: Không thể kết nối Telegram. Hệ thống vẫn sẽ chạy nhưng không gửi được cảnh báo.")
        choice = input("Tiếp tục? (y/n): ")
        if choice.lower() != 'y':
            return
    
    # Khởi tạo và chạy detector
    try:
        detector = IntrusionDetector()
        detector.run()
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()