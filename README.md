# 🚨 Intrusion Warning System with AI Detection

Hệ thống cảnh báo xâm nhập thông minh sử dụng Python, OpenCV, YOLO AI và Telegram với điều khiển từ xa.

## ✨ Tính Năng Mới - AI Object Detection

🤖 **Phân biệt đối tượng thông minh:**
- 👥 **Người lớn** (Adults)
- 👶 **Trẻ em** (Children)  
- � **Động vật** (Animals)

🚨 **Hệ thống cảnh báo đa cấp:**
- **LOW** - Chỉ có động vật
- **MEDIUM** - Có trẻ em hoặc 1 người lớn  
- **HIGH** - Có nhiều người lớn (≥2)
- **CRITICAL** - Có cả người lớn và trẻ em

## �🚀 Khởi Động Nhanh

```bash
# Cài đặt dependencies (bao gồm AI)
pip install -r requirements.txt

# Chạy hệ thống hoàn chỉnh (Main + Web Dashboard)
scripts\start_complete_system.bat

# Hoặc chạy từng phần
scripts\start_main_system.bat        # Chỉ hệ thống chính
scripts\start_web_dashboard.bat      # Chỉ web dashboard

# Test AI detection
python test_ai_integration.py
```

## 📱 Điều Khiển Telegram

- **`/chup`** - Chụp ảnh ngay lập tức
- **`/mo`** - Bật camera giám sát  
- **`/thoat`** - Tắt camera giám sát

## ⌨️ Phím Tắt

- **`q`** - Thoát chương trình
- **`a`** - **Bật/tắt AI Detection** 🤖
- **`s`** - Chụp ảnh thủ công
- **`r`** - Reset/học lại ảnh nền
- **`m`** - Test phát hiện chuyển động
- **`+`/`=`** - Tăng ngưỡng phát hiện (+500px)
- **`-`** - Giảm ngưỡng phát hiện (-500px)
- **`0`** - Reset ngưỡng về 5000px

## 🔧 Cấu Hình

Chỉnh sửa file `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 📚 Tài Liệu Chi Tiết

Xem thư mục [`how_it_works/`](how_it_works/) để tìm hiểu:

- **[HOW_IT_WORKS.md](how_it_works/HOW_IT_WORKS.md)** - Cách hệ thống phát hiện chuyển động
- **[AI_DETECTION_GUIDE.md](how_it_works/AI_DETECTION_GUIDE.md)** - **Hướng dẫn AI Detection** 🤖
- **[REAL_TIME_CONTROL.md](how_it_works/REAL_TIME_CONTROL.md)** - Giao diện điều khiển real-time
- **[SETUP.md](how_it_works/SETUP.md)** - Hướng dẫn cài đặt chi tiết
- **[REMOTE_GUIDE.md](how_it_works/REMOTE_GUIDE.md)** - Hướng dẫn điều khiển từ xa

## 🎯 Ứng Dụng Big Data & Machine Learning

Dự án này tích hợp các công nghệ hiện đại:
- **Computer Vision**: OpenCV cho xử lý ảnh real-time
- **Deep Learning**: YOLO v8 cho object detection
- **Machine Learning**: Thuật toán phân loại đối tượng
- **Real-time Processing**: Xử lý dữ liệu video streaming
- **Big Data**: Log và phân tích dữ liệu cảnh báo

## 🔥 Performance

- **FPS**: 25-30 (motion only) | 20-25 (with AI)
- **Latency**: <50ms cho detection
- **Memory**: ~200-300MB (với AI)
- **CPU**: Tối ưu cho real-time processing
- **[WEB_GUIDE.md](how_it_works/WEB_GUIDE.md)** - Hướng dẫn web dashboard
- **[PROJECT_STRUCTURE.md](how_it_works/PROJECT_STRUCTURE.md)** - Cấu trúc dự án

## 🌐 Web Dashboard

Truy cập `http://localhost:5000` để xem dashboard quản lý sự kiện, ảnh và thống kê.

---

**⚡ Hệ thống phát hiện chuyển động thông minh, gửi cảnh báo qua Telegram, có web dashboard quản lý!**