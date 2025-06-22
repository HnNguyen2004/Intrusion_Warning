# 🚀 Hướng dẫn setup nhanh Intrusion Warning System

## Bước 1: Cài đặt dependencies (✅ Đã hoàn thành)
```bash
pip install -r requirements.txt
```

## Bước 2: Cấu hình Telegram Bot

### 2.1. Tạo Telegram Bot
1. Mở Telegram và tìm kiếm **@BotFather**
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (VD: "My Intrusion Warning Bot")
4. Đặt username cho bot (VD: "my_intrusion_warning_bot")
5. **Lưu Bot Token** được cung cấp

### 2.2. Lấy Chat ID
1. Gửi tin nhắn bất kỳ cho bot vừa tạo
2. Mở trình duyệt và truy cập:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
   (Thay `<BOT_TOKEN>` bằng token thực)
3. Tìm dòng có `"chat":{"id":XXXXXXX}` và **lưu số ID này**

### 2.3. Cấu hình trong code
Mở file `config.py` và thay đổi:
```python
TELEGRAM_BOT_TOKEN = "1234567890:AABBCCDDEEFFaabbccddeeffgghhiijjkk"  # Bot Token từ BotFather
TELEGRAM_CHAT_ID = "987654321"                                      # Chat ID từ API
```

## Bước 3: Test hệ thống
```bash
python demo.py
```

## Bước 4: Chạy hệ thống chính
```bash
python main.py
```

## Các phím tắt khi chạy:
- **q**: Thoát
- **s**: Chụp ảnh thủ công
- **r**: Reset background

## Khắc phục sự cố thường gặp:

### ❌ Camera không hoạt động:
- Đảm bảo camera không bị ứng dụng khác sử dụng
- Thử thay đổi `CAMERA_INDEX` trong `config.py` (0, 1, 2...)

### ❌ Telegram không gửi được:
- Kiểm tra Bot Token và Chat ID
- Đảm bảo đã gửi tin nhắn cho bot trước
- Kiểm tra kết nối internet

### ❌ Quá nhạy hoặc không nhạy:
- Điều chỉnh `MOTION_THRESHOLD` trong `config.py`
- Nhấn `r` để reset background khi chạy

---

**🎯 Mục tiêu**: Hệ thống sẽ phát hiện chuyển động qua camera và gửi cảnh báo kèm ảnh qua Telegram!
