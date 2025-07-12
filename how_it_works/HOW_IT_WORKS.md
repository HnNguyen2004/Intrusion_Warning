# 🔍 Cách hoạt động của hệ thống phát hiện chuyển động

## 📐 **Thông số cơ bản**

### Camera Resolution:
- **Độ phân giải**: 640 × 480 pixels
- **Tổng pixels**: 307,200 pixels
- **Frame rate**: ~20 FPS (mỗi giây 20 ảnh)

### Ngưỡng hiện tại (config.py):
```python
MOTION_THRESHOLD = 21000  # pixels (6.8% của tổng frame)
CONTOUR_MIN_AREA = 500    # pixels tối thiểu cho 1 vùng
```

## 🧠 **Thuật toán phát hiện từng bước**

### **Bước 1: Chuyển đổi màu sắc**
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
- **Input**: Frame màu RGB (640×480×3 = 921,600 giá trị)
- **Output**: Frame xám (640×480 = 307,200 giá trị)
- **Mục đích**: Giảm dữ liệu, dễ xử lý

### **Bước 2: Làm mờ Gaussian**
```python
gray = cv2.GaussianBlur(gray, (21, 21), 0)
```
- **Kernel**: 21×21 pixels
- **Mục đích**: Giảm nhiễu, làm mịn ảnh
- **Kết quả**: Ảnh ít bị nhiễu sáng

### **Bước 3: So sánh với ảnh nền**
```python
frame_delta = cv2.absdiff(self.background, gray)
```
- **background**: Ảnh nền ban đầu (không có chuyển động)
- **gray**: Ảnh hiện tại
- **frame_delta**: Độ khác biệt giữa 2 ảnh

**Ví dụ cụ thể:**
```
Pixel ảnh nền:     120 (độ xám)
Pixel ảnh hiện tại: 180 (độ xám)
Khác biệt:         |180 - 120| = 60
```

### **Bước 4: Ngưỡng hóa (Threshold)**
```python
thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
```
- **Ngưỡng**: 30 (độ xám)
- **Logic**: 
  - Nếu khác biệt > 30 → Pixel = 255 (trắng = có chuyển động)
  - Nếu khác biệt ≤ 30 → Pixel = 0 (đen = không chuyển động)

**Ví dụ:**
```
frame_delta = 60 > 30 → thresh = 255 (CÓ chuyển động)
frame_delta = 15 ≤ 30 → thresh = 0   (KHÔNG chuyển động)
```

### **Bước 5: Mở rộng vùng (Dilation)**
```python
thresh = cv2.dilate(thresh, None, iterations=2)
```
- **Mục đích**: Kết nối các pixel rời rạc thành vùng lớn hơn
- **Kết quả**: Các vùng chuyển động được "phình to"

### **Bước 6: Tìm contours (đường viền)**
```python
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- **Contour**: Đường viền bao quanh vùng chuyển động
- **Kết quả**: Danh sách các vùng chuyển động riêng biệt

### **Bước 7: Tính diện tích**
```python
for contour in contours:
    area = cv2.contourArea(contour)
    if area < CONTOUR_MIN_AREA:  # < 500 pixels
        continue  # Bỏ qua vùng quá nhỏ
    motion_area += area  # Cộng dồn diện tích
```

## 📊 **Ví dụ thực tế**

### **Scenario 1: Người đi ngang qua camera**
```
Tổng pixels frame:     307,200
Pixels có chuyển động: 25,000 (người + bóng)
Phần trăm:            25,000 / 307,200 = 8.1%
Kết quả:              25,000 > 21,000 → ✅ GỬI CẢNH BÁO
```

### **Scenario 2: Mèo chạy qua**
```
Tổng pixels frame:     307,200  
Pixels có chuyển động: 3,500 (con mèo)
Phần trăm:            3,500 / 307,200 = 1.1%
Kết quả:              3,500 < 21,000 → ❌ KHÔNG gửi cảnh báo
```

### **Scenario 3: Xe hơi đi qua**
```
Tổng pixels frame:     307,200
Pixels có chuyển động: 45,000 (xe lớn)
Phần trăm:            45,000 / 307,200 = 14.6%
Kết quả:              45,000 > 21,000 → ✅ GỬI CẢNH BÁO
```

### **Scenario 4: Lá cây rung**
```
Tổng pixels frame:     307,200
Pixels có chuyển động: 8,000 (lá cây)
Phần trăm:            8,000 / 307,200 = 2.6%
Kết quả:              8,000 < 21,000 → ❌ KHÔNG gửi cảnh báo
```

## ⚙️ **Tùy chỉnh độ nhạy**

### **Giảm false positive (ít cảnh báo giả)**:
```python
MOTION_THRESHOLD = 25000  # Tăng ngưỡng (8.1% → 8.7%)
CONTOUR_MIN_AREA = 800    # Tăng diện tích tối thiểu
```

### **Tăng độ nhạy (phát hiện nhiều hơn)**:
```python  
MOTION_THRESHOLD = 15000  # Giảm ngưỡng (6.8% → 4.9%)
CONTOUR_MIN_AREA = 300    # Giảm diện tích tối thiểu
```

## 🎯 **Các yếu tố ảnh hưởng**

### **Môi trường:**
- **Ánh sáng thay đổi**: Tạo nhiều pixel thay đổi
- **Gió thổi**: Lá cây, rèm cửa chuyển động
- **Bóng**: Tạo thêm vùng chuyển động

### **Đối tượng:**
- **Kích thước**: Người lớn > trẻ em > thú cưng
- **Tốc độ**: Chạy > đi > đứng yên
- **Màu sắc**: Tương phản với nền

### **Camera:**
- **Góc nhìn**: Rộng hơn = dễ phát hiện hơn
- **Độ phân giải**: Cao hơn = chính xác hơn
- **Vị trí**: Chiều cao, góc đặt

## 🧪 **Debug và testing**

### **Nhấn phím 'm' để test:**
```python
test_area = 8500.0  # Giả lập 8500 pixels chuyển động
# 8500 < 21000 → Sẽ KHÔNG gửi cảnh báo
```

### **Xem thông tin debug:**
```
👁️ Phát hiện chuyển động nhỏ: 8500 pixels (< 21000, không gửi cảnh báo)
```

### **Khi có cảnh báo thật:**
```
🚨 Phát hiện xâm nhập! Diện tích: 25000.0 pixels
```

## 💡 **Tips tối ưu**

1. **Đặt camera ở vị trí cố định** - Tránh rung lắc
2. **Tránh nguồn sáng mạnh** - Đèn, cửa sổ
3. **Test nhiều thời điểm** - Sáng, tối, có gió
4. **Điều chỉnh từ từ** - Thay đổi ngưỡng từng chút
5. **Sử dụng phím 'r'** - Reset nền khi môi trường thay đổi

---

**🎯 Tóm lại**: Hệ thống đếm số pixel thay đổi so với ảnh nền. Nếu > 21,000 pixels (6.8% frame) thì gửi cảnh báo!
