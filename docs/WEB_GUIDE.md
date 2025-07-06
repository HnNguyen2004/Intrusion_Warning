# 🌐 Web Management System

Hệ thống quản lý web cho Intrusion Warning System được xây dựng với Flask + Vue.js.

## ✨ Tính năng

- 📊 **Dashboard** - Tổng quan hệ thống với thống kê real-time
- 📋 **Event Management** - Xem danh sách sự kiện phát hiện xâm nhập
- 📷 **Image Gallery** - Thư viện ảnh cảnh báo với thumbnail
- 📈 **Analytics** - Biểu đồ thống kê theo ngày và giờ
- 🔄 **Real-time Updates** - Tự động cập nhật mỗi 30 giây
- 📱 **Responsive** - Giao diện thích ứng mọi thiết bị

## 🚀 Cách chạy

### Phương pháp 1: Sử dụng script (Khuyến nghị)
```bash
# Chạy file batch
start_web.bat
```

### Phương pháp 2: Chạy thủ công
```bash
# Cài đặt dependencies
pip install flask flask-cors flask-restful

# Chạy Flask API
python web_api.py
```

### Truy cập giao diện web:
- **Web UI**: http://localhost:5000/web
- **API Docs**: http://localhost:5000/

## 📡 API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/events` | GET | Lấy danh sách sự kiện |
| `/api/images` | GET | Lấy danh sách ảnh |
| `/api/images/<filename>` | GET | Lấy ảnh cụ thể |
| `/api/images/<filename>/thumbnail` | GET | Lấy thumbnail ảnh |
| `/api/stats` | GET | Thống kê hệ thống |
| `/api/system/status` | GET | Trạng thái hệ thống |
| `/api/config` | GET | Cấu hình hiện tại |

## 🎯 Cách sử dụng

### 1. Dashboard
- Xem tổng quan số liệu: tổng sự kiện, sự kiện hôm nay, số ảnh, tỷ lệ thành công
- Kiểm tra trạng thái hệ thống (đang chạy/dừng)

### 2. Tab Sự kiện
- Xem danh sách tất cả sự kiện phát hiện
- Thông tin chi tiết: thời gian, độ tin cậy, trạng thái gửi cảnh báo
- Click "Xem ảnh" để mở ảnh cảnh báo

### 3. Tab Ảnh cảnh báo
- Thư viện ảnh dạng lưới với thumbnail
- Click vào ảnh để xem full size
- Tải ảnh về máy

### 4. Tab Thống kê
- Biểu đồ sự kiện theo 7 ngày qua
- Biểu đồ sự kiện theo 24 giờ trong ngày
- Phân tích xu hướng

## 🔧 Tùy chỉnh

### Thay đổi port:
Sửa trong file `web_api.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Thay 5000 thành port khác
```

### Thay đổi tần suất auto-refresh:
Sửa trong file `web_frontend/index.html`:
```javascript
setInterval(async () => {
    // ...
}, 60000);  // Thay 30000 (30s) thành 60000 (60s)
```

## 🐛 Troubleshooting

### Lỗi không thể kết nối API:
- Kiểm tra Flask server đã chạy chưa
- Kiểm tra port 5000 có bị chiếm dụng không
- Thử truy cập http://localhost:5000/ để test API

### Không có dữ liệu hiển thị:
- Đảm bảo hệ thống chính đã chạy và tạo file log
- Kiểm tra file `intrusion_log.csv` có tồn tại không
- Chạy `python main_with_remote.py` trước để tạo dữ liệu

### Ảnh không hiển thị:
- Kiểm tra thư mục `alert_images/` có ảnh không
- Đảm bảo quyền đọc file ảnh
- Thử nhấn F12 > Console để xem lỗi JavaScript

## 🚀 Mở rộng

### Thêm tính năng mới:
1. Thêm API endpoint trong `web_api.py`
2. Thêm giao diện trong `web_frontend/index.html`
3. Thêm xử lý JavaScript

### Deploy production:
- Sử dụng **Gunicorn** cho Flask
- **Nginx** làm reverse proxy
- **PM2** để quản lý process

---

**💡 Tip**: Mở cả hệ thống chính (`main_with_remote.py`) và web system để có trải nghiệm đầy đủ!
