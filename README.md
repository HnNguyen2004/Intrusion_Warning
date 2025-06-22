# 🏠 Intrusion Warning System

Hệ thống cảnh báo xâm nhập thông minh sử dụng camera để phát hiện chuyển động và gửi cảnh báo qua Telegram.

## ✨ Tính năng

- 📹 **Phát hiện chuyển động** qua camera real-time
- 🚨 **Gửi cảnh báo Telegram** ngay lập tức kèm ảnh
- 📊 **Ghi log** lịch sử phát hiện vào file CSV
- 🎮 **Giao diện giám sát** trực quan
- ⚙️ **Cấu hình linh hoạt** và dễ mở rộng
- 🔒 **Chống spam** với thời gian cooldown

## 🚀 Cài đặt

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình Telegram Bot

#### Tạo bot mới:
1. Nhắn tin cho [@BotFather](https://t.me/botfather) trên Telegram
2. Gửi lệnh `/newbot`
3. Đặt tên và username cho bot
4. Lưu **Bot Token** được cung cấp

#### Lấy Chat ID:
1. Nhắn tin bất kỳ cho bot vừa tạo
2. Truy cập: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Tìm `"chat":{"id":XXXXXXX}` và lưu **Chat ID**

#### Cập nhật cấu hình:
Mở file `config.py` và thay đổi:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Thay bằng Bot Token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Thay bằng Chat ID
```

## 🎯 Sử dụng

### Chạy hệ thống:
```bash
python main.py
```

### Phím tắt trong giao diện:
- **`q`**: Thoát chương trình
- **`s`**: Chụp ảnh thủ công
- **`r`**: Reset background (hiệu chỉnh lại phát hiện)

## 📁 Cấu trúc dự án

```
Intrusion_Warning/
├── main.py                 # File chạy chính
├── config.py              # Cấu hình hệ thống
├── intrusion_detector.py  # Module phát hiện xâm nhập
├── telegram_handler.py    # Module xử lý Telegram
├── logger.py              # Module ghi log
├── requirements.txt       # Dependencies
├── README.md              # Hướng dẫn
├── alert_images/          # Thư mục lưu ảnh cảnh báo
├── intrusion_log.csv      # File log CSV
└── system.log             # File log hệ thống
```

## ⚙️ Cấu hình

Các tham số có thể điều chỉnh trong `config.py`:

```python
# Camera
CAMERA_INDEX = 0              # Index của camera (0 = camera mặc định)

# Phát hiện chuyển động
MOTION_THRESHOLD = 5000       # Ngưỡng diện tích để kích hoạt cảnh báo
CONTOUR_MIN_AREA = 500        # Diện tích tối thiểu của contour

# File paths
LOG_FILE = "intrusion_log.csv"           # File log CSV
ALERT_IMAGES_DIR = "alert_images"        # Thư mục lưu ảnh
```

## 📊 Log và lịch sử

### File CSV (`intrusion_log.csv`):
- Timestamp: Thời gian phát hiện
- Detection_Type: Loại phát hiện
- Confidence: Độ tin cậy (0-1)
- Image_Path: Đường dẫn ảnh
- Alert_Sent: Đã gửi cảnh báo hay chưa

### File log hệ thống (`system.log`):
- Ghi lại các sự kiện hệ thống
- Lỗi và cảnh báo
- Trạng thái kết nối

## 🔧 Khắc phục sự cố

### Camera không hoạt động:
- Kiểm tra `CAMERA_INDEX` trong `config.py`
- Thử các giá trị khác: 0, 1, 2...
- Đảm bảo camera không bị ứng dụng khác sử dụng

### Telegram không gửi được:
- Kiểm tra Bot Token và Chat ID
- Đảm bảo có kết nối internet
- Kiểm tra bot đã được start chưa

### Phát hiện quá nhạy/không nhạy:
- Điều chỉnh `MOTION_THRESHOLD`
- Điều chỉnh `CONTOUR_MIN_AREA`
- Nhấn `r` để reset background

## 🔮 Mở rộng tương lai

- [ ] Tích hợp YOLO để phân biệt người/vật
- [ ] Web interface để giám sát từ xa
- [ ] Hỗ trợ nhiều camera
- [ ] Cảnh báo qua email
- [ ] Phân tích hành vi
- [ ] Lưu trữ cloud

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

---

**Lưu ý**: Đây là hệ thống demo. Để sử dụng trong môi trường thực tế, cần bổ sung thêm các tính năng bảo mật và tối ưu hóa.