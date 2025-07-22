import cv2

print("🔍 Đang dò tìm camera...")

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print(f"✓ Camera sẵn sàng ở index {i}")
        cap.release()
    else:
        print(f"✗ Không có camera ở index {i}")
