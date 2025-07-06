"""
Flask Web API cho Intrusion Warning System
Quản lý sự kiện, logs và ảnh cảnh báo
"""

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import os
import csv
import json
from datetime import datetime, timedelta
import glob
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)  # Cho phép Vue.js gọi API

# Import từ hệ thống chính
import sys
sys.path.append('.')
from config import ALERT_IMAGES_DIR, LOG_FILE
from logger import IntrusionLogger

class WebAPI:
    def __init__(self):
        self.logger = IntrusionLogger(LOG_FILE)
        
    def get_events(self, limit=50):
        """Lấy danh sách sự kiện từ CSV"""
        events = []
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        events.append({
                            'timestamp': row.get('timestamp', ''),
                            'detection_type': row.get('detection_type', ''),
                            'confidence': float(row.get('confidence', 0)),
                            'image_path': row.get('image_path', ''),
                            'alert_sent': row.get('alert_sent', 'False') == 'True'
                        })
                        
                # Sắp xếp theo thời gian mới nhất trước
                events.sort(key=lambda x: x['timestamp'], reverse=True)
                return events[:limit]
        except Exception as e:
            print(f"Error reading events: {e}")
        return events
    
    def get_images(self):
        """Lấy danh sách ảnh cảnh báo"""
        images = []
        try:
            pattern = os.path.join(ALERT_IMAGES_DIR, "*.jpg")
            files = glob.glob(pattern)
            files.sort(key=os.path.getmtime, reverse=True)  # Mới nhất trước
            
            for file_path in files:
                filename = os.path.basename(file_path)
                file_stat = os.stat(file_path)
                images.append({
                    'filename': filename,
                    'path': file_path,
                    'size': file_stat.st_size,
                    'created': datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                })
        except Exception as e:
            print(f"Error reading images: {e}")
        return images
    
    def get_stats(self):
        """Lấy thống kê hệ thống"""
        events = self.get_events(1000)  # Lấy nhiều để tính toán
        
        # Tính toán thống kê
        total_events = len(events)
        today_events = len([e for e in events if e['timestamp'].startswith(datetime.now().strftime('%Y-%m-%d'))])
        
        # Thống kê theo ngày trong tuần qua
        week_stats = {}
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            week_stats[date] = len([e for e in events if e['timestamp'].startswith(date)])
        
        # Thống kê theo giờ trong ngày
        hour_stats = {}
        for hour in range(24):
            hour_str = f"{hour:02d}"
            hour_stats[hour_str] = len([e for e in events if f" {hour_str}:" in e['timestamp']])
        
        return {
            'total_events': total_events,
            'today_events': today_events,
            'week_stats': week_stats,
            'hour_stats': hour_stats,
            'alert_success_rate': round(len([e for e in events if e['alert_sent']]) / max(total_events, 1) * 100, 1)
        }

# Khởi tạo API
web_api = WebAPI()

# Routes API
@app.route('/api/events')
def get_events():
    """API lấy danh sách sự kiện"""
    try:
        limit = request.args.get('limit', 50, type=int)
        events = web_api.get_events(limit)
        return jsonify({
            'success': True,
            'data': events,
            'total': len(events)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/images')
def get_images():
    """API lấy danh sách ảnh"""
    try:
        images = web_api.get_images()
        return jsonify({
            'success': True,
            'data': images,
            'total': len(images)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/images/<filename>')
def get_image(filename):
    """API lấy ảnh cụ thể"""
    try:
        return send_from_directory(ALERT_IMAGES_DIR, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@app.route('/api/images/<filename>/thumbnail')
def get_image_thumbnail(filename):
    """API lấy thumbnail ảnh"""
    try:
        file_path = os.path.join(ALERT_IMAGES_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        # Tạo thumbnail
        with Image.open(file_path) as img:
            img.thumbnail((200, 200))
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=85)
            img_io.seek(0)
            
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """API lấy thống kê hệ thống"""
    try:
        stats = web_api.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system/status')
def get_system_status():
    """API kiểm tra trạng thái hệ thống"""
    try:
        # Kiểm tra xem có file log mới không (trong 5 phút qua)
        is_running = False
        last_activity = "Không có hoạt động"
        
        if os.path.exists(LOG_FILE):
            events = web_api.get_events(1)
            if events:
                last_event_time = datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
                time_diff = datetime.now() - last_event_time
                if time_diff.total_seconds() < 300:  # 5 phút
                    is_running = True
                last_activity = events[0]['timestamp']
        
        return jsonify({
            'success': True,
            'data': {
                'is_running': is_running,
                'last_activity': last_activity,
                'images_count': len(web_api.get_images()),
                'events_count': len(web_api.get_events()),
                'log_file_exists': os.path.exists(LOG_FILE),
                'images_dir_exists': os.path.exists(ALERT_IMAGES_DIR)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config')
def get_config():
    """API lấy cấu hình hiện tại"""
    try:
        from config import MOTION_THRESHOLD, CONTOUR_MIN_AREA, CAMERA_INDEX
        return jsonify({
            'success': True,
            'data': {
                'motion_threshold': MOTION_THRESHOLD,
                'contour_min_area': CONTOUR_MIN_AREA,
                'camera_index': CAMERA_INDEX
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """Trang chủ API"""
    return jsonify({
        'message': 'Intrusion Warning System API',
        'version': '1.0.0',
        'web_ui': '/web',
        'endpoints': {
            '/api/events': 'Lấy danh sách sự kiện',
            '/api/images': 'Lấy danh sách ảnh',
            '/api/images/<filename>': 'Lấy ảnh cụ thể',
            '/api/stats': 'Thống kê hệ thống',
            '/api/system/status': 'Trạng thái hệ thống',
            '/api/config': 'Cấu hình hiện tại'
        }
    })

@app.route('/web')
def web_ui():
    """Giao diện web"""
    return send_file('web_frontend/index.html')

if __name__ == '__main__':
    # Đảm bảo thư mục alert_images tồn tại
    os.makedirs(ALERT_IMAGES_DIR, exist_ok=True)
    
    print("🌐 Starting Intrusion Warning Web API...")
    print("📡 API URL: http://localhost:5000")
    print("📊 Endpoints:")
    print("   GET /api/events - Danh sách sự kiện")
    print("   GET /api/images - Danh sách ảnh")
    print("   GET /api/stats - Thống kê")
    print("   GET /api/system/status - Trạng thái hệ thống")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
