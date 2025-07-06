# 📁 Project Structure

```
Intrusion_Warning/
├── 🚀 CORE SYSTEM
│   ├── main_with_remote.py           # 🔥 MAIN FILE - Hệ thống chính
│   ├── config.py                     # ⚙️ Cấu hình hệ thống
│   ├── intrusion_detector.py         # 👁️ Module phát hiện xâm nhập
│   ├── telegram_handler.py           # 📱 Module xử lý Telegram
│   ├── logger.py                     # 📝 Module ghi log
│   └── remote_control.py             # 🎮 Module điều khiển từ xa
│
├── 🌐 WEB SYSTEM
│   ├── web_api.py                    # 🔗 Flask API backend
│   └── web_frontend/
│       └── index.html                # 🖥️ Vue.js frontend
│
├── 🔐 CONFIGURATION
│   ├── .env                          # 🔑 Environment variables (IGNORED)
│   ├── .env.example                  # 📋 Template cấu hình
│   ├── requirements.txt              # 📦 Python dependencies
│   └── .gitignore                    # 🚫 Git ignore rules
│
├── 🚀 STARTUP SCRIPTS
│   ├── start_complete_system.bat     # 🔥 MAIN STARTUP - Chạy cả hệ thống
│   ├── start_main_system.bat         # 📹 Chỉ chạy main system
│   └── start_web_dashboard.bat       # 🌐 Chỉ chạy web dashboard
│
├── 📊 DATA & STORAGE
│   ├── alert_images/                 # 📷 Thư mục ảnh cảnh báo (IGNORED)
│   │   └── .gitkeep                  # 📁 Giữ cấu trúc thư mục
│   └── intrusion_log.csv             # 📊 File log CSV (IGNORED)
│
├── 📖 DOCUMENTATION
│   ├── README.md                     # 📖 Hướng dẫn chính
│   └── docs/                         # 📚 Thư mục tài liệu chi tiết
│       ├── HUONG_DAN_CHI_TIET.md     # 🇻🇳 Hướng dẫn tiếng Việt
│       ├── SETUP.md                  # 🔧 Hướng dẫn cài đặt
│       ├── REMOTE_GUIDE.md           # 📱 Hướng dẫn điều khiển từ xa
│       ├── WEB_GUIDE.md              # 🌐 Hướng dẫn web system
│       ├── PROXY_GUIDE.md            # 🌐 Hướng dẫn proxy
│       └── TAI_SAO_RESET.md          # ❓ FAQ
│
└── 🔄 VERSION CONTROL
    ├── .git/                         # 📂 Git repository
    └── .gitkeep files                # 📁 Giữ cấu trúc thư mục trống
```

## 🎯 Files chính cần quan tâm

### 🔥 **CORE FILES** (Bắt buộc)
- `main_with_remote.py` - File chính để chạy
- `config.py` - Cấu hình hệ thống
- `intrusion_detector.py` - Logic phát hiện
- `telegram_handler.py` - Xử lý Telegram
- `logger.py` - Ghi log
- `remote_control.py` - Điều khiển từ xa

### 🌐 **WEB FILES** (Optional nhưng khuyên dùng)
- `web_api.py` - API backend
- `web_frontend/index.html` - Giao diện web

### 🚀 **STARTUP FILES** (Tiện lợi)
- `start_complete_system.bat` - Script chính
- `start_main_system.bat` - Chỉ main system
- `start_web_dashboard.bat` - Chỉ web dashboard

### 🔐 **CONFIG FILES** (Quan trọng)
- `.env` - Chứa token/chat ID (BỊ IGNORE)
- `.env.example` - Template
- `requirements.txt` - Dependencies

## ⚡ Quick Start

1. **Setup**: Copy `.env.example` → `.env` và điền thông tin
2. **Install**: `pip install -r requirements.txt`
3. **Run**: Double-click `start_complete_system.bat`
4. **Access**: http://localhost:5000/web

## 🗑️ Files đã được dọn dẹp

❌ **Đã xóa**:
- `demo.py` - File demo cũ
- `demo_motion.py` - Demo motion detection
- `get_chat_id.py` - Script lấy chat ID (không cần nữa)
- `system.log` - Log cũ
- `intrusion_log.csv` - Log cũ (sẽ tự tạo lại)
- `start_web.bat` - Script cũ
- `__pycache__/` - Python cache

📚 **Di chuyển vào docs/**:
- Tất cả file `.md` hướng dẫn chi tiết

🖼️ **Đã dọn dẹp**:
- Tất cả ảnh cũ trong `alert_images/` (giữ `.gitkeep`)

## 🎊 Kết quả

✅ **Workspace sạch sẽ và có tổ chức**
✅ **Chỉ giữ lại files cần thiết**  
✅ **Documentation được sắp xếp gọn gàng**
✅ **Git ignore hoàn chỉnh**
✅ **Ready for production**
