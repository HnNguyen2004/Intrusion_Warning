import requests
import logging
from datetime import datetime
import os
import time

class TelegramHandler:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        # Danh sách proxy để thử (cho Việt Nam)
        self.proxy_configs = [
            None,  # Không proxy (thử trước)
            {  # Cloudflare WARP SOCKS5
                'http': 'socks5://127.0.0.1:40000',
                'https': 'socks5://127.0.0.1:40000'
            },
            {  # Cloudflare WARP HTTP
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080'
            }
        ]
        
        self.working_proxy = None
        self.timeout = 15
        self.max_retries = 2
        
    def _find_working_proxy(self):
        """Tìm proxy hoạt động"""
        if self.working_proxy is not None:
            return self.working_proxy
            
        print("🔍 Đang tìm proxy hoạt động...")
        
        for i, proxy in enumerate(self.proxy_configs):
            try:
                print(f"   Thử cấu hình {i+1}/{len(self.proxy_configs)}...")
                
                test_url = f"{self.base_url}/getMe"
                response = requests.get(
                    test_url, 
                    proxies=proxy, 
                    timeout=self.timeout,
                    verify=False  # Bỏ qua SSL verification
                )
                
                if response.status_code == 200:
                    self.working_proxy = proxy
                    proxy_name = "Direct" if proxy is None else f"Proxy {proxy}"
                    print(f"✅ Tìm thấy kết nối hoạt động: {proxy_name}")
                    return proxy
                    
            except Exception as e:
                print(f"   ❌ Cấu hình {i+1} thất bại: {str(e)[:50]}...")
                continue
        
        print("❌ Không tìm thấy proxy hoạt động")
        return None
        
    def _make_request(self, method, url, **kwargs):
        """Thực hiện request với proxy tự động"""
        proxy = self._find_working_proxy()
        
        for attempt in range(self.max_retries):
            try:
                kwargs['timeout'] = self.timeout
                kwargs['proxies'] = proxy
                kwargs['verify'] = False  # Bỏ qua SSL verification
                
                response = getattr(requests, method)(url, **kwargs)
                
                if response.status_code == 200:
                    return response
                else:
                    logging.warning(f"Telegram API returned status {response.status_code}")
                    
            except Exception as e:
                logging.warning(f"Request attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    
        return None
        
    def send_message(self, message):
        """Gửi tin nhắn text qua Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = self._make_request('post', url, data=data)
            
            if response:
                logging.info("Telegram message sent successfully")
                return True
            else:
                logging.error("Failed to send Telegram message")
                return False
                
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False
    
    def send_photo(self, image_path, caption=""):
        """Gửi ảnh qua Telegram"""
        try:
            url = f"{self.base_url}/sendPhoto"
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = self._make_request('post', url, files=files, data=data)
                
                if response:
                    logging.info("Telegram photo sent successfully")
                    return True
                else:
                    logging.error("Failed to send Telegram photo")
                    return False
                    
        except Exception as e:
            logging.error(f"Error sending photo: {e}")
            return False
    
    def send_alert(self, detection_type, image_path=None):
        """Gửi cảnh báo xâm nhập"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🚨 <b>CẢNH BÁO XÂM NHẬP</b> 🚨\n\n"
        message += f"⏰ Thời gian: {timestamp}\n"
        message += f"🔍 Loại phát hiện: {detection_type}\n"
        message += f"📍 Vị trí: Cửa ra vào chính"
        
        # Gửi tin nhắn
        message_sent = self.send_message(message)
        
        # Gửi ảnh nếu có
        photo_sent = True
        if image_path and os.path.exists(image_path):
            photo_sent = self.send_photo(image_path, f"Ảnh phát hiện xâm nhập - {timestamp}")
        
        return message_sent and photo_sent
        
    def test_connection(self):
        """Test kết nối Telegram"""
        try:
            proxy = self._find_working_proxy()
            if proxy is None:
                return False
                
            url = f"{self.base_url}/getMe"
            response = requests.get(url, proxies=proxy, timeout=self.timeout, verify=False)
            
            if response.status_code == 200:
                bot_info = response.json()
                bot_name = bot_info.get('result', {}).get('username', 'Unknown')
                logging.info(f"Telegram bot connected: {bot_name}")
                return True
            else:
                logging.error("Failed to connect to Telegram bot")
                return False
                
        except Exception as e:
            logging.error(f"Error testing Telegram connection: {e}")
            return False
