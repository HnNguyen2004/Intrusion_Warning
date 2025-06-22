"""
Demo script để hiểu rõ cách phát hiện chuyển động
Có chú thích tiếng Việt chi tiết từng bước
"""

import cv2
import numpy as np
from datetime import datetime
from config import CAMERA_INDEX, MOTION_THRESHOLD, CONTOUR_MIN_AREA

def demo_motion_detection():
    print("🎯 DEMO: Hiểu cách phát hiện chuyển động")
    print("=" * 60)
    print("📝 Hướng dẫn:")
    print("- Trạng thái 'MONITORING': Không có chuyển động")
    print("- Trạng thái 'MOTION DETECTED': Có chuyển động")
    print("- Hộp xanh lá: Vùng chuyển động")
    print("- Diện tích hiển thị ở góc trái")
    print("- Ngưỡng cảnh báo:", MOTION_THRESHOLD, "pixels")
    print("=" * 60)
    print("🎮 Phím tắt:")
    print("- 'q': Thoát")
    print("- 'r': Reset background")
    print("- 's': Giảm ngưỡng (dễ kích hoạt hơn)")
    print("- 'h': Tăng ngưỡng (khó kích hoạt hơn)")
    print("=" * 60)
    
    # Bước 1: Mở camera (kết nối với webcam)
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Không thể mở camera")
        return
    
    # Biến lưu trữ ảnh nền và các thông số
    background = None  # Ảnh nền để so sánh
    motion_threshold = MOTION_THRESHOLD  # Ngưỡng kích hoạt cảnh báo
    alert_count = 0  # Đếm số lần cảnh báo
    
    print("🟢 Bắt đầu demo... Di chuyển trước camera để test!")
    
    while True:
        # Bước 2: Đọc frame (khung hình) từ camera
        ret, frame = cap.read()
        if not ret:
            break
        
        # Bước 3: Xử lý ảnh để phát hiện chuyển động
        # Chuyển đổi sang ảnh xám (grayscale) để dễ xử lý
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Làm mờ ảnh để giảm nhiễu (noise)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
          # Bước 4: Khởi tạo ảnh nền (background) lần đầu
        if background is None:
            background = gray  # Lưu frame đầu tiên làm nền
            print("🎯 Dang hoc anh nen moi... Vui long dung yen!")
            continue
        
        # Bước 5: Tính toán sự khác biệt giữa frame hiện tại và nền
        # Tìm vùng có sự thay đổi (chuyển động)
        frame_delta = cv2.absdiff(background, gray)
        
        # Chuyển đổi thành ảnh nhị phân (đen trắng)
        # Pixel > 30 = trắng (có chuyển động), < 30 = đen (không đổi)
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        
        # Làm dày các vùng trắng để dễ phát hiện
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Bước 6: Tìm các vùng chuyển động (contours)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Khởi tạo biến để tính toán
        total_motion_area = 0  # Tổng diện tích chuyển động
        motion_detected = False  # Có phát hiện chuyển động không?
        contour_count = 0  # Số lượng vùng chuyển động
        
        # Bước 7: Vẽ hộp xanh lá cho từng vùng chuyển động
        for contour in contours:
            # Tính diện tích của vùng chuyển động
            area = cv2.contourArea(contour)
            
            # Bỏ qua các vùng quá nhỏ (có thể là nhiễu)
            if area < CONTOUR_MIN_AREA:
                continue
                
            contour_count += 1
            total_motion_area += area
            
            # Tìm hình chữ nhật bao quanh vùng chuyển động
            (x, y, w, h) = cv2.boundingRect(contour)
            
            # Vẽ hộp màu xanh lá quanh vùng chuyển động
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
              # Hiển thị diện tích của từng vùng bên trong hộp
            cv2.putText(frame, f"Dien tich: {int(area)}", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
          # Bước 8: Kiểm tra có kích hoạt cảnh báo không
        if total_motion_area > motion_threshold:
            motion_detected = True
            alert_count += 1
            print(f"🚨 CANH BAO #{alert_count}: Dien tich chuyen dong = {total_motion_area:.1f} > {motion_threshold}")        # Bước 9: Hiển thị thông tin trên màn hình
        # Hiển thị trạng thái (ĐANG GIÁM SÁT hoặc PHÁT HIỆN CHUYỂN ĐỘNG)
        if background is None:
            status_text = "DANG HOC ANH NEN..."
            status_color = (0, 255, 255)  # Màu vàng
        else:
            status_text = "PHAT HIEN CHUYEN DONG" if motion_detected else "DANG GIAM SAT"
            status_color = (0, 0, 255) if motion_detected else (0, 255, 0)  # Đỏ hoặc xanh lá
        
        cv2.putText(frame, f"Trang thai: {status_text}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Hiển thị tổng diện tích chuyển động hiện tại
        cv2.putText(frame, f"Dien tich chuyen dong: {total_motion_area:.1f}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Hiển thị ngưỡng cảnh báo
        cv2.putText(frame, f"Nguong canh bao: {motion_threshold}", 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Hiển thị số lượng vùng chuyển động
        cv2.putText(frame, f"So vung chuyen dong: {contour_count}", 
                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Hiển thị số lần đã cảnh báo
        cv2.putText(frame, f"So lan canh bao: {alert_count}", 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Hiển thị thời gian hiện tại
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, 
                   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
          # Hiển thị hướng dẫn sử dụng phím
        cv2.putText(frame, "Nhan 'q':Thoat 'r':Reset 's':Giam nguong 'h':Tang nguong", 
                   (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Hiển thị cửa sổ video
        cv2.imshow('Demo Phat Hien Chuyen Dong - He Thong Canh Bao Xam Nhap', frame)
        
        # Bước 10: Cập nhật ảnh nền từ từ (học môi trường mới)
        # Trộn 95% ảnh nền cũ + 5% ảnh hiện tại
        background = cv2.addWeighted(background, 0.95, gray, 0.05, 0)
        
        # Bước 11: Xử lý phím bấm từ người dùng
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break  # Thoát chương trình        elif key == ord('r'):
            background = None  # Reset ảnh nền
            print("🔄 Da reset anh nen - He thong se hoc lai moi truong moi!")
            print("   👉 Dung yen 3-5 giay de he thong hoc anh nen moi")
        elif key == ord('s'):
            motion_threshold = max(1000, motion_threshold - 1000)  # Giảm ngưỡng
            print(f"⬇️  Nguong giam xuong: {motion_threshold}")
        elif key == ord('h'):
            motion_threshold += 1000  # Tăng ngưỡng
            print(f"⬆️  Nguong tang len: {motion_threshold}")
      # Bước 12: Dọn dẹp khi kết thúc
    cap.release()  # Đóng camera
    cv2.destroyAllWindows()  # Đóng cửa sổ
    
    print(f"\n📊 KET QUA DEMO:")
    print(f"- Tong so canh bao: {alert_count}")
    print(f"- Nguong cuoi cung: {motion_threshold}")
    print("✅ Demo hoan thanh!")

if __name__ == "__main__":
    demo_motion_detection()
