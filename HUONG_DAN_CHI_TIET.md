# 📚 HƯỚNG DẪN CHI TIẾT: Cách hoạt động của hệ thống phát hiện xâm nhập

## 🎯 Tổng quan hoạt động

Hệ thống **Intrusion Warning** hoạt động dựa trên nguyên lý **phát hiện chuyển động**:

1. **Học ảnh nền** (background) khi không có ai
2. **So sánh** frame hiện tại với ảnh nền  
3. **Tìm vùng khác biệt** (chuyển động)
4. **Vẽ hộp xanh lá** quanh vùng chuyển động
5. **Kích hoạt cảnh báo** khi chuyển động đủ lớn

---

## 🔍 Giải thích từng bước trong code

### **Bước 1: Chuẩn bị**
```python
cap = cv2.VideoCapture(0)  # Mở camera
background = None          # Ảnh nền chưa có
```
- Kết nối với webcam (camera số 0)
- Khởi tạo biến lưu ảnh nền

### **Bước 2: Đọc frame từ camera**
```python
ret, frame = cap.read()
```
- Đọc 1 khung hình từ camera
- `ret` = True nếu đọc thành công
- `frame` = ảnh màu 3 kênh (BGR)

### **Bước 3: Chuyển đổi ảnh**
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Chuyển sang xám
gray = cv2.GaussianBlur(gray, (21, 21), 0)      # Làm mờ
```
- **Tại sao chuyển sang xám?** Dễ xử lý hơn, tốc độ nhanh hơn
- **Tại sao làm mờ?** Giảm nhiễu, tránh phát hiện nhầm

### **Bước 4: Tạo ảnh nền lần đầu**
```python
if background is None:
    background = gray  # Lưu frame đầu tiên
```
- Frame đầu tiên = ảnh nền
- **Quan trọng**: Đứng yên khi chương trình khởi động!

### **Bước 5: Tính sự khác biệt**
```python
frame_delta = cv2.absdiff(background, gray)
```
- So sánh pixel từng điểm
- Pixel thay đổi nhiều = có chuyển động
- Kết quả: ảnh xám có vùng sáng (chuyển động) và tối (không đổi)

### **Bước 6: Tạo ảnh nhị phân**
```python
thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
```
- **30**: Ngưỡng phân biệt (có thể điều chỉnh)
- Pixel > 30 → Trắng (255) = có chuyển động
- Pixel ≤ 30 → Đen (0) = không đổi

### **Bước 7: Làm dày vùng trắng**
```python
thresh = cv2.dilate(thresh, None, iterations=2)
```
- Nối các điểm trắng gần nhau
- Tạo vùng chuyển động liền mạch

### **Bước 8: Tìm contour (viền)**
```python
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- Tìm đường viền các vùng trắng
- Mỗi contour = 1 vùng chuyển động

### **Bước 9: Vẽ hộp và tính diện tích**
```python
for contour in contours:
    area = cv2.contourArea(contour)      # Tính diện tích
    if area < 500: continue              # Bỏ qua vùng nhỏ
    
    (x, y, w, h) = cv2.boundingRect(contour)  # Tìm hình chữ nhật bao quanh
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Vẽ hộp xanh
```

### **Bước 10: Kiểm tra cảnh báo**
```python
if total_motion_area > 5000:
    print("🚨 CẢNH BÁO!")
    # Chụp ảnh và gửi Telegram
```

### **Bước 11: Cập nhật ảnh nền**
```python
background = cv2.addWeighted(background, 0.95, gray, 0.05, 0)
```
- **95% ảnh nền cũ + 5% ảnh hiện tại**
- Học dần môi trường mới (ánh sáng thay đổi, vật cố định mới)

---

## 🎨 Ý nghĩa màu sắc trên màn hình

| Màu sắc | Ý nghĩa |
|---------|---------|
| 🟢 **Hộp xanh lá** | Vùng phát hiện chuyển động |
| 🔴 **Chữ đỏ "MOTION DETECTED"** | Đang có chuyển động lớn |
| 🟢 **Chữ xanh "MONITORING"** | Đang giám sát, không có chuyển động |
| ⚪ **Chữ trắng** | Thông tin hệ thống |
| 🟡 **Chữ vàng** | Số lần cảnh báo |

---

## 📊 Thông số quan trọng

### **MOTION_THRESHOLD = 5000**
- Ngưỡng kích hoạt cảnh báo
- Càng nhỏ = càng nhạy
- Càng lớn = càng khó kích hoạt

### **CONTOUR_MIN_AREA = 500**  
- Diện tích tối thiểu để vẽ hộp
- Bỏ qua các chuyển động quá nhỏ (nhiễu)

### **Threshold = 30**
- Độ nhạy phát hiện thay đổi pixel
- Môi trường ổn định: có thể dùng 20-25
- Môi trường nhiều nhiễu: nên dùng 35-40

---

## 🎮 Cách sử dụng thực tế

### **Khi chạy lần đầu:**
1. **Đứng yên** 3-5 giây để hệ thống học ảnh nền
2. **Di chuyển chậm** để xem hộp xanh lá xuất hiện
3. **Di chuyển nhanh/nhiều** để kích hoạt cảnh báo

### **Nếu quá nhạy (cảnh báo liên tục):**
```python
MOTION_THRESHOLD = 8000    # Tăng lên
CONTOUR_MIN_AREA = 800     # Tăng lên
```

### **Nếu không nhạy (không phát hiện):**
```python
MOTION_THRESHOLD = 2000    # Giảm xuống  
CONTOUR_MIN_AREA = 200     # Giảm xuống
```

### **Reset khi môi trường thay đổi:**
- Nhấn phím **'r'** để reset ảnh nền
- Hoặc restart chương trình

---

## 🔧 Các trường hợp đặc biệt

### **Ánh sáng thay đổi:**
- Hệ thống tự động thích ứng từ từ (95% cũ + 5% mới)
- Thay đổi đột ngột → nhấn 'r' để reset

### **Có vật cố định mới:**
- Đưa vật vào → nhấn 'r' → đứng yên 5 giây
- Hệ thống sẽ học vật mới làm phần của nền

### **Camera rung:**
- Gắn camera chắc chắn
- Tăng MOTION_THRESHOLD để tránh false alarm

---

## 💡 Mẹo tối ưu

1. **Đặt camera ở góc cao**, nhìn xuống cửa
2. **Tránh nguồn sáng thay đổi** (cửa sổ, đèn nhấp nháy)
3. **Test kỹ** trước khi sử dụng thực tế
4. **Backup cấu hình** khi đã tối ưu xong

**🎯 Mục tiêu cuối cùng: Phát hiện người xâm nhập, không phát hiện nhầm!**
