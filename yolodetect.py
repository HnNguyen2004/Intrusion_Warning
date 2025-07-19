from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
import numpy as np
from telegram_utils import send_telegram
import datetime
import threading
import asyncio


def isInside(points, centroid):
    polygon = Polygon(points)
    centroid_point = Point(centroid)
    print(f"Centroid: {centroid}, Polygon points: {points}")
    print(f"Polygon contains centroid: {polygon.contains(centroid_point)}")
    return polygon.contains(centroid_point)


def send_telegram_sync():
    """Wrapper function để gọi async send_telegram từ thread"""
    try:
        asyncio.run(send_telegram())
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")


class YoloDetect():
    def __init__(self, detect_class="person", frame_width=1280, frame_height=720):
        # Parameters
        self.classnames_file = "model/classnames.txt"
        self.weights_file = "model/yolov4-tiny.weights"
        self.config_file = "model/yolov4-tiny.cfg"
        # Giảm threshold để detect dễ dàng hơn
        self.conf_threshold = 0.3  # Giảm từ 0.5 xuống 0.3
        self.nms_threshold = 0.4
        self.detect_class = detect_class
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = 1 / 255
        self.model = cv2.dnn.readNet(self.weights_file, self.config_file)
        self.classes = None
        self.output_layers = None
        self.read_class_file()
        self.get_output_layers()
        self.last_alert = None
        self.alert_telegram_each = 15  # seconds
        
        # Thêm tracking để cải thiện độ ổn định
        self.previous_detections = []
        self.tracking_threshold = 0.6  # Threshold cho tracking

    def read_class_file(self):
        with open(self.classnames_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def get_output_layers(self):
        layer_names = self.model.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.model.getUnconnectedOutLayers()]

    def calculate_centroid_robust(self, x, y, x_plus_w, y_plus_h, confidence):
        """Tính toán centroid với nhiều phương pháp khác nhau"""
        # Phương pháp 1: Centroid thông thường
        centroid_x = (x + x_plus_w) / 2.0
        centroid_y = (y + y_plus_h) / 2.0
        
        # Phương pháp 2: Weighted centroid dựa trên confidence
        if confidence > 0.7:
            # Với confidence cao, sử dụng centroid thông thường
            pass
        elif confidence > 0.5:
            # Với confidence trung bình, điều chỉnh nhẹ
            centroid_x += np.random.normal(0, 2)  # Thêm noise nhỏ
            centroid_y += np.random.normal(0, 2)
        else:
            # Với confidence thấp, sử dụng tracking
            if self.previous_detections:
                # Lấy centroid từ frame trước
                prev_centroid = self.previous_detections[-1]
                centroid_x = (centroid_x + prev_centroid[0]) / 2
                centroid_y = (centroid_y + prev_centroid[1]) / 2
        
        return (int(centroid_x), int(centroid_y))

    def draw_prediction(self, img, class_id, x, y, x_plus_w, y_plus_h, points, confidence):
        label = str(self.classes[class_id])
        color = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Tinh toan centroid với phương pháp robust
        centroid = self.calculate_centroid_robust(x, y, x_plus_w, y_plus_h, confidence)
        
        # Lưu centroid cho tracking
        self.previous_detections.append(centroid)
        if len(self.previous_detections) > 5:  # Giữ 5 frame gần nhất
            self.previous_detections.pop(0)
        
        # Vẽ centroid với màu khác để dễ nhận biết
        cv2.circle(img, centroid, 5, (255, 0, 0), -1)  # Màu đỏ cho centroid
        
        # Debug: vẽ bounding box với màu khác
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), (0, 255, 0), 2)  # Màu xanh cho bounding box
        
        # Debug: hiển thị tọa độ centroid và confidence
        cv2.putText(img, f"C({centroid[0]},{centroid[1]}) conf:{confidence:.2f}", 
                   (centroid[0] + 10, centroid[1] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

        # Kiểm tra nhiều điểm trong bounding box thay vì chỉ centroid
        is_inside = self.check_multiple_points_in_box(x, y, x_plus_w, y_plus_h, points, centroid)
        
        if is_inside:
            img = self.alert(img)

        return is_inside

    def check_multiple_points_in_box(self, x, y, x_plus_w, y_plus_h, points, centroid):
        """Kiểm tra nhiều điểm trong bounding box để tăng độ tin cậy"""
        polygon = Polygon(points)
        
        # Kiểm tra centroid chính
        if polygon.contains(Point(centroid)):
            return True
        
        # Kiểm tra các điểm khác trong bounding box
        check_points = [
            centroid,  # Centroid chính
            (x + 10, y + 10),  # Góc trên trái
            (x_plus_w - 10, y + 10),  # Góc trên phải
            (x + 10, y_plus_h - 10),  # Góc dưới trái
            (x_plus_w - 10, y_plus_h - 10),  # Góc dưới phải
            ((x + x_plus_w) // 2, y + 10),  # Điểm giữa cạnh trên
            ((x + x_plus_w) // 2, y_plus_h - 10),  # Điểm giữa cạnh dưới
        ]
        
        inside_count = 0
        for point in check_points:
            if polygon.contains(Point(point)):
                inside_count += 1
                # Vẽ điểm được kiểm tra
                cv2.circle(img, point, 3, (0, 255, 255), -1)  # Màu vàng
        
        # Nếu có ít nhất 2 điểm trong polygon thì coi như detect được
        return inside_count >= 2

    def alert(self, img):
        cv2.putText(img, "ALARM!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # New thread to send telegram after 15 seconds
        if (self.last_alert is None) or (
                (datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_telegram_each):
            self.last_alert = datetime.datetime.utcnow()
            cv2.imwrite("alert.png", cv2.resize(img, dsize=None, fx=0.2, fy=0.2))
            # Sử dụng wrapper function thay vì gọi trực tiếp async function
            thread = threading.Thread(target=send_telegram_sync)
            thread.start()
        return img

    def detect(self, frame, points):
        # Lấy kích thước thực tế của frame
        actual_height, actual_width = frame.shape[:2]
        
        blob = cv2.dnn.blobFromImage(frame, self.scale, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.output_layers)

        # Loc cac object trong khung hinh
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if (confidence >= self.conf_threshold) and (self.classes[class_id] == self.detect_class):
                    # Sử dụng kích thước thực tế của frame thay vì self.frame_width/height
                    center_x = int(detection[0] * actual_width)
                    center_y = int(detection[1] * actual_height)
                    w = int(detection[2] * actual_width)
                    h = int(detection[3] * actual_height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)

        for i in indices:
            box = boxes[i]
            x = int(box[0])  # Chuyển thành int ngay từ đầu
            y = int(box[1])
            w = int(box[2])
            h = int(box[3])
            x_plus_w = x + w
            y_plus_h = y + h
            confidence = confidences[i]
            self.draw_prediction(frame, class_ids[i], x, y, x_plus_w, y_plus_h, points, confidence)

        return frame