# 🔐 Hướng dẫn Setup cho Developers

## 📥 Clone và Setup

### 1. Clone repository:
```bash
git clone <your-repo-url>
cd Intrusion_Warning
```

### 2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### 3. Tạo file .env:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 4. Cấu hình Telegram:

#### Tạo Telegram Bot:
1. Nhắn tin cho [@BotFather](https://t.me/botfather)
2. Gửi `/newbot` và làm theo hướng dẫn
3. Lưu **Bot Token**

#### Lấy Chat ID:
```bash
# Cách dễ nhất - dùng script có sẵn:
python get_chat_id.py
```

#### Cập nhật file .env:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id_from_script
```

### 5. Test hệ thống:
```bash
# Test demo chuyển động
python demo_motion.py

# Test toàn bộ hệ thống
python demo.py

# Chạy hệ thống thật
python main.py
```

## 🔒 Bảo mật

- **KHÔNG** commit file `.env` lên Git
- **KHÔNG** hardcode token/chat ID trong code
- File `.gitignore` đã được cấu hình để bảo vệ thông tin nhạy cảm

## 📁 Cấu trúc Project

```
├── main.py              # File chính
├── config.py            # Cấu hình (đọc từ .env)
├── intrusion_detector.py  # Logic phát hiện
├── telegram_handler.py  # Xử lý Telegram
├── logger.py            # Ghi log
├── demo.py              # Demo tổng thể
├── demo_motion.py       # Demo phát hiện chuyển động
├── get_chat_id.py       # Utility lấy Chat ID
├── requirements.txt     # Dependencies
├── .env.example         # Template cấu hình
└── .env                 # Cấu hình thật (không commit)
```
