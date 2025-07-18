"""
AI Object Detection Module - YOLO Integration
Phân biệt người lớn/trẻ em/động vật cho hệ thống cảnh báo xâm nhập
"""

import cv2
import numpy as np
from ultralytics import YOLO
import torch
from datetime import datetime
import os

class AIObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """Khởi tạo AI Object Detector với YOLO"""
        print("🤖 Đang khởi tạo AI Object Detection...")
        try:
            # Load YOLO model
            self.model = YOLO(model_path)
            print(f"✅ Đã load YOLO model: {model_path}")
            
            # Định nghĩa classes cần phát hiện
            self.target_classes = {
                0: 'person',      # Người
                15: 'cat',        # Mèo
                16: 'dog',        # Chó  
                17: 'horse',      # Ngựa
                18: 'sheep',      # Cừu
                19: 'cow',        # Bò
                20: 'elephant',   # Voi
                21: 'bear',       # Gấu
                22: 'zebra',      # Ngựa vằn
                23: 'giraffe'     # Hươu cao cổ
            }
            
            # Phân loại theo kích thước và nguy hiểm
            self.classification_rules = {
                'adults': {'min_area': 8000, 'alert_level': 'HIGH'},
                'children': {'min_area': 3000, 'max_area': 8000, 'alert_level': 'MEDIUM'},
                'large_animals': {'classes': ['horse', 'cow', 'elephant', 'bear'], 'alert_level': 'HIGH'},
                'small_animals': {'classes': ['cat', 'dog'], 'alert_level': 'LOW'},
                'wild_animals': {'classes': ['zebra', 'giraffe', 'elephant', 'bear'], 'alert_level': 'CRITICAL'}
            }
            
            print("🎯 AI Detection sẵn sàng phân tích!")
            
        except Exception as e:
            print(f"❌ Lỗi khởi tạo YOLO: {e}")
            self.model = None
    
    def detect_and_classify(self, frame, draw_boxes=False):
        """
        Phát hiện và phân loại objects trong frame
        Returns: (detections, analysis_result)
        """
        if self.model is None:
            return [], {'total_objects': 0, 'alert_level': 'NONE'}
        
        try:
            # Chạy YOLO detection
            results = self.model(frame, verbose=False)
            
            detections = []
            analysis = {
                'adults': 0,
                'children': 0,
                'large_animals': 0,
                'small_animals': 0,
                'wild_animals': 0,
                'total_objects': 0,
                'alert_level': 'NONE',
                'objects_detected': []
            }
            
            # Xử lý kết quả
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Lấy thông tin box
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        # Chỉ xử lý classes quan tâm và confidence > 0.5
                        if class_id in self.target_classes and confidence > 0.5:
                            class_name = self.target_classes[class_id]
                            area = (x2 - x1) * (y2 - y1)
                            
                            detection = {
                                'class_name': class_name,
                                'confidence': float(confidence),
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'area': float(area),
                                'classification': self._classify_object(class_name, area)
                            }
                            
                            detections.append(detection)
                            analysis['total_objects'] += 1
                            analysis['objects_detected'].append(class_name)
                            
                            # Phân loại cho analysis
                            classification = detection['classification']
                            if classification in analysis:
                                analysis[classification] += 1
                            
                            # Vẽ bounding box nếu cần
                            if draw_boxes:
                                self._draw_detection_box(frame, detection)
            
            # Xác định mức độ cảnh báo
            analysis['alert_level'] = self._determine_alert_level(analysis)
            
            return detections, analysis
            
        except Exception as e:
            print(f"❌ Lỗi AI detection: {e}")
            return [], {'total_objects': 0, 'alert_level': 'NONE'}
    
    def _classify_object(self, class_name, area):
        """Phân loại object dựa trên class và kích thước"""
        if class_name == 'person':
            if area >= 8000:
                return 'adults'
            elif area >= 3000:
                return 'children'
            else:
                return 'children'  # Person nhỏ coi như trẻ em
        
        elif class_name in ['horse', 'cow', 'elephant', 'bear']:
            return 'large_animals'
        elif class_name in ['cat', 'dog']:
            return 'small_animals'
        elif class_name in ['zebra', 'giraffe', 'elephant', 'bear']:
            return 'wild_animals'
        else:
            return 'unknown'
    
    def _determine_alert_level(self, analysis):
        """Xác định mức độ cảnh báo dựa trên phân tích"""
        if analysis['wild_animals'] > 0:
            return 'CRITICAL'
        elif analysis['adults'] > 0 or analysis['large_animals'] > 0:
            return 'HIGH'
        elif analysis['children'] > 0:
            return 'MEDIUM'
        elif analysis['small_animals'] > 0:
            return 'LOW'
        else:
            return 'NONE'
    
    def _draw_detection_box(self, frame, detection):
        """Vẽ bounding box với thông tin phân loại"""
        x1, y1, x2, y2 = detection['bbox']
        class_name = detection['class_name']
        confidence = detection['confidence']
        classification = detection['classification']
        
        # Màu sắc theo phân loại
        colors = {
            'adults': (0, 0, 255),        # Đỏ - Người lớn
            'children': (0, 165, 255),    # Cam - Trẻ em  
            'large_animals': (0, 255, 255), # Vàng - Động vật lớn
            'small_animals': (0, 255, 0), # Xanh lá - Động vật nhỏ
            'wild_animals': (255, 0, 255), # Tím - Động vật hoang dã
            'unknown': (128, 128, 128)    # Xám - Không xác định
        }
        
        color = colors.get(classification, (255, 255, 255))
        
        # Vẽ bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Tạo label
        if classification == 'adults':
            label = f"👤 Người lớn ({confidence:.2f})"
        elif classification == 'children':
            label = f"👶 Trẻ em ({confidence:.2f})"
        elif classification in ['large_animals', 'wild_animals']:
            label = f"🐾 {class_name.title()} ({confidence:.2f})"
        elif classification == 'small_animals':
            label = f"🐱 {class_name.title()} ({confidence:.2f})"
        else:
            label = f"{class_name} ({confidence:.2f})"
        
        # Vẽ label background
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                     (x1 + label_size[0], y1), color, -1)
        
        # Vẽ text
        cv2.putText(frame, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def format_detection_message(self, detections, analysis):
        """Tạo message mô tả kết quả phát hiện"""
        if analysis['total_objects'] == 0:
            return "Không phát hiện đối tượng nào"
        
        message_parts = []
        
        # Thống kê theo loại
        if analysis['adults'] > 0:
            message_parts.append(f"👤 {analysis['adults']} người lớn")
        if analysis['children'] > 0:
            message_parts.append(f"👶 {analysis['children']} trẻ em")
        if analysis['large_animals'] > 0:
            message_parts.append(f"🐾 {analysis['large_animals']} động vật lớn")
        if analysis['small_animals'] > 0:
            message_parts.append(f"🐱 {analysis['small_animals']} động vật nhỏ")
        if analysis['wild_animals'] > 0:
            message_parts.append(f"🦁 {analysis['wild_animals']} động vật hoang dã")
        
        # Tạo message
        if message_parts:
            message = "🤖 AI phát hiện: " + ", ".join(message_parts)
        else:
            message = f"🤖 AI phát hiện: {analysis['total_objects']} đối tượng"
        
        # Thêm mức độ cảnh báo
        alert_emojis = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': '💡',
            'NONE': '✅'
        }
        
        emoji = alert_emojis.get(analysis['alert_level'], '❓')
        message += f"\n{emoji} Mức độ: {analysis['alert_level']}"
        
        return message

# Test function để demo
def test_ai_detection():
    """Test AI detection với webcam"""
    detector = AIObjectDetector()
    
    if detector.model is None:
        print("❌ Không thể test AI detection - model không load được")
        return
    
    cap = cv2.VideoCapture(0)
    print("📹 Bắt đầu test AI detection (nhấn 'q' để thoát)")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect và classify
        detections, analysis = detector.detect_and_classify(frame, draw_boxes=True)
        
        # Hiển thị thông tin
        message = detector.format_detection_message(detections, analysis)
        print(f"🔍 {message}")
        
        # Hiển thị frame
        cv2.putText(frame, f"Objects: {analysis['total_objects']}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Alert: {analysis['alert_level']}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('AI Object Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_ai_detection()
