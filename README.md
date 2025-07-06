# 🏠 Intrusion Warning System

Hệ thống cảnh báo xâm nhập thông minh sử dụng camera để phát hiện chuyển động và gửi cảnh báo qua Telegram với khả năng điều khiển từ xa.

## ✨ Tính năng

- 📹 **Phát hiện chuyển động** qua camera real-time với ngưỡng tùy chỉnh
- 🚨 **Gửi cảnh báo Telegram** ngay lập tức kèm ảnh không có box phát hiện
- � **Điều khiển từ xa** qua Telegram với các lệnh `/chup`, `/mo`, `/thoat`
- �📊 **Ghi log** lịch sử phát hiện vào file CSV tự động
- 🎮 **Giao diện giám sát** trực quan với box phát hiện màu xanh
- ⚙️ **Cấu hình linh hoạt** và tối ưu hiệu suất
- � **Ngưỡng thông minh**: Chỉ gửi cảnh báo khi > 5000 pixels

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
```bash
# Cách 1: Sử dụng script có sẵn
python get_chat_id.py

# Cách 2: Thủ công
# 1. Nhắn tin bất kỳ cho bot vừa tạo
# 2. Truy cập: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
# 3. Tìm "chat":{"id":XXXXXXX} và lưu Chat ID
```

#### Cập nhật cấu hình:
1. Sao chép file `.env.example` thành `.env`:
```bash
copy .env.example .env
```

2. Chỉnh sửa file `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**⚠️ LƯU Ý**: File `.env` chứa thông tin nhạy cảm và sẽ không được đưa lên Git.

## 🎯 Sử dụng

### Chạy hệ thống:
```bash
python main_with_remote.py
```

### Phím tắt trong giao diện:
- **`q`**: Thoát chương trình
- **`s`**: Chụp ảnh thủ công và gửi qua Telegram
- **`r`**: Reset background (học lại môi trường)
- **`m`**: Test gửi cảnh báo (giả lập phát hiện)

### Điều khiển từ xa qua Telegram:
- **`/chup`**: Chụp ảnh từ xa (không tắt chương trình)
- **`/mo`**: Bật camera giám sát
- **`/thoat`**: Tắt camera giám sát

### Logic hoạt động:
- **Diện tích > 5000 pixels**: Gửi cảnh báo + ảnh + ghi log
- **Diện tích ≤ 5000 pixels**: Chỉ hiển thị thông báo, không gửi Telegram
- **Ảnh Telegram**: Không có box xanh (nhìn rõ mặt)
- **Ảnh trên màn hình**: Có box xanh (để debug)

## 📁 Cấu trúc dự án

```
Intrusion_Warning/
├── 🚀 CORE SYSTEM
│   ├── main_with_remote.py           # � MAIN FILE - Hệ thống chính
│   ├── config.py                     # ⚙️ Cấu hình hệ thống  
│   ├── intrusion_detector.py         # 👁️ Module phát hiện xâm nhập
│   ├── telegram_handler.py           # 📱 Module xử lý Telegram
│   ├── logger.py                     # 📝 Module ghi log
│   └── remote_control.py             # 🎮 Module điều khiển từ xa
│
├── 🌐 WEB SYSTEM
│   ├── web_api.py                    # 🔗 Flask API backend
│   └── web_frontend/index.html       # �️ Vue.js frontend
│
├── 🚀 STARTUP SCRIPTS  
│   ├── start_complete_system.bat     # 🔥 MAIN STARTUP
│   ├── start_main_system.bat         # � Main system only
│   └── start_web_dashboard.bat       # 🌐 Web dashboard only
│
├── 🔐 CONFIG & DATA
│   ├── .env                          # � Environment variables  
│   ├── requirements.txt              # � Dependencies
│   ├── alert_images/                 # 📷 Ảnh cảnh báo (auto-generated)
│   └── intrusion_log.csv             # 📊 Log CSV (auto-generated)
│
└── 📖 DOCUMENTATION
    ├── README.md                     # 📖 Hướng dẫn chính (file này)
    ├── PROJECT_STRUCTURE.md          # 📁 Chi tiết cấu trúc dự án
    └── docs/                         # � Tài liệu chi tiết
```

> 📋 **Chi tiết đầy đủ**: Xem `PROJECT_STRUCTURE.md`

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

### Điều chỉnh độ nhạy:
- **Tăng MOTION_THRESHOLD** (5000 → 8000): Giảm cảnh báo, chỉ phát hiện chuyển động lớn
- **Giảm MOTION_THRESHOLD** (5000 → 3000): Tăng độ nhạy, phát hiện chuyển động nhỏ hơn
- **Tăng CONTOUR_MIN_AREA**: Lọc bỏ nhiễu nhỏ

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
- Cắm sạc laptop để đảm bảo hiệu suất

### Telegram không gửi được:
- Chạy `python test_telegram.py` để kiểm tra kết nối
- Kiểm tra Bot Token và Chat ID trong file `.env`
- Đảm bảo có kết nối internet
- Kiểm tra bot đã được start chưa (gửi `/start` cho bot)

### Camera bị lag:
- Hệ thống đã tối ưu: xử lý mỗi 5 frame, 20 FPS
- Cắm sạc laptop gaming
- Đóng các ứng dụng khác đang chạy
- Giảm độ sáng màn hình để tiết kiệm tài nguyên

### Phát hiện quá nhạy/không nhạy:
- Điều chỉnh `MOTION_THRESHOLD` trong `config.py`
- Nhấn `r` để reset background khi thay đổi môi trường
- Chuyển động > 5000 pixels mới gửi cảnh báo

### Bot điều khiển từ xa không hoạt động:
- Kiểm tra token/chat ID trong `.env`
- Đảm bảo bot đã được start
- Thử gửi lệnh `/chup` để test

## 🔮 Tính năng đã hoàn thành

- ✅ **Phát hiện chuyển động** với ngưỡng thông minh
- ✅ **Gửi ảnh Telegram** không có box phát hiện
- ✅ **Điều khiển từ xa** qua Telegram hoàn chỉnh
- ✅ **Ghi log tự động** vào CSV
- ✅ **Tối ưu hiệu suất** giảm lag camera
- ✅ **Giao diện thân thiện** với phím tắt
- ✅ **Reset background** thông minh
- ✅ **Test kết nối** Telegram tích hợp

## 🔮 Mở rộng tương lai

- [ ] Tích hợp YOLO để phân biệt người/vật
- [ ] Web interface để giám sát từ xa
- [ ] Hỗ trợ nhiều camera
- [ ] Cảnh báo qua email
- [ ] Phân tích hành vi nâng cao
- [ ] Lưu trữ cloud (Google Drive, AWS)

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

---

## 🚀 Cách sử dụng nhanh

### 🔥 **Phương pháp 1: Chạy hệ thống hoàn chỉnh (Khuyến nghị)**
```cmd
# Chạy cả Main System + Web Dashboard cùng lúc
start_complete_system.bat
```
**Kết quả:**
- 📹 **Window 1**: Main system (camera + Telegram)
- 🌐 **Window 2**: Web dashboard (http://localhost:5000/web)
- 🌐 **Browser**: Tự động mở giao diện web

### 🔧 **Phương pháp 2: Chạy riêng từng hệ thống**

**Hệ thống chính:**
```cmd
start_main_system.bat
# HOẶC: python main_with_remote.py
```

**Web dashboard (chạy trong terminal khác):**
```cmd
start_web_dashboard.bat  
# HOẶC: python web_api.py
```

### 🎯 **Workflow đầy đủ:**

1. **🚀 Khởi động**: `start_complete_system.bat`
2. **📹 Kiểm tra**: Main system window hiển thị camera
3. **🌐 Truy cập**: http://localhost:5000/web
4. **📱 Test**: Gửi `/chup` qua Telegram hoặc nhấn `m`
5. **📊 Giám sát**: Theo dõi qua web dashboard

### 📱 **Điều khiển từ xa qua Telegram:**
- `/chup` - Chụp ảnh từ xa
- `/mo` - Bật camera giám sát  
- `/thoat` - Tắt camera giám sát

### 🎮 **Điều khiển trực tiếp:**
- `q` - Thoát chương trình
- `s` - Chụp ảnh thủ công  
- `r` - Reset background
- `m` - Test phát hiện

### 🌐 **Web Dashboard:**
- **Dashboard**: Thống kê tổng quan
- **Events**: Danh sách sự kiện phát hiện
- **Images**: Thư viện ảnh cảnh báo
- **Stats**: Biểu đồ phân tích

**Lưu ý**: Hệ thống hoàn chỉnh và ổn định. Main file để chạy là `start_complete_system.bat`.