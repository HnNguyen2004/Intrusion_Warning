import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Camera Configuration
CAMERA_INDEX = 0  # 0 for default camera
MOTION_THRESHOLD = 21000  # Threshold for motion detection
CONTOUR_MIN_AREA = 500   # Minimum area for valid contour

# AI Detection Configuration
USE_AI_DETECTION = True   # Enable/disable AI object detection
AI_MODEL_PATH = 'yolov8n.pt'  # YOLO model path
AI_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for AI detection
AI_DETECTION_INTERVAL = 5      # Run AI detection every N frames

# Alert Level Thresholds
ALERT_THRESHOLDS = {
    'CRITICAL': 'Immediate alert + call emergency',
    'HIGH': 'Immediate alert',
    'MEDIUM': 'Standard alert',
    'LOW': 'Log only, no alert',
    'NONE': 'No action'
}

# File paths
LOG_FILE = "intrusion_log.csv"
ALERT_IMAGES_DIR = "alert_images"

# Create directories if they don't exist
os.makedirs(ALERT_IMAGES_DIR, exist_ok=True)
