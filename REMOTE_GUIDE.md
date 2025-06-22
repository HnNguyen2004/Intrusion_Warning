# 📱 Hướng Dẫn Điều Khiển Từ Xa Qua Telegram

## 🚀 Hướng dẫn sử dụng

Hệ thống đã được cập nhật để hỗ trợ điều khiển từ xa qua Telegram. Dưới đây là các lệnh và cách sử dụng:

### Các lệnh điều khiển từ xa:

| Lệnh | Chức năng |
|------|-----------|
| `/chup` | Chụp ảnh từ camera và gửi về Telegram |
| `/mo` | Bật camera giám sát (mở cửa sổ hiển thị) |
| `/thoat` | Tắt camera giám sát |
| `/start` hoặc `/help` | Xem hướng dẫn |

### Cách sử dụng:

1. **Khởi động hệ thống:**
   ```
   python main_with_remote.py
   ```

2. **Bot Telegram sẽ tự động khởi động**

3. **Chat với bot:**
   - Gửi lệnh `/start` để xem hướng dẫn
   - Gửi lệnh `/chup` để chụp ảnh và nhận về Telegram
   - Gửi lệnh `/mo` để bật camera giám sát
   - Gửi lệnh `/thoat` để tắt camera giám sát

## 🔒 Bảo mật

Bot chỉ phản hồi cho chat ID được cấu hình trong file `.env`. Người khác không thể điều khiển hệ thống của bạn.

## 🚨 Xử lý lỗi phổ biến:

1. **Lỗi `draw_motion_overlay` không tồn tại:**
   - Đã được sửa trong phiên bản mới

2. **Lỗi `log_error` không tồn tại:**
   - Đã được sửa trong phiên bản mới

3. **Camera không mở được:**
   - Kiểm tra camera có đang được sử dụng bởi phần mềm khác không
   - Đổi `CAMERA_INDEX` trong config.py

4. **Bot không phản hồi:**
   - Kiểm tra kết nối internet
   - Kiểm tra token có đúng không

## 📋 Chức năng đã cải tiến:

- ✅ Điều khiển từ xa thông qua Telegram
- ✅ Nhận ảnh giám sát về điện thoại
- ✅ Bật/tắt camera từ xa
- ✅ Chụp ảnh từ xa

*Chú ý: Hệ thống giờ đây đã hoạt động hoàn toàn và tương thích với điều khiển từ xa!*
