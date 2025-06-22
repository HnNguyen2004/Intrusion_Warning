# 🌐 Hướng dẫn cấu hình Proxy cho Telegram (Việt Nam)

## Tại sao cần proxy?
Ở Việt Nam, Telegram bị chặn nên cần sử dụng proxy để kết nối.

## Cách 1: Sử dụng Cloudflare WARP (Đã cài)

### Kiểm tra WARP đang hoạt động:
1. Mở Cloudflare WARP app
2. Đảm bảo trạng thái là "Connected"
3. Kiểm tra IP: https://1.1.1.1/help

### Cấu hình trong code:
Nếu WARP vẫn không hoạt động, hãy cấu hình proxy thủ công trong `telegram_handler.py`:

```python
# Trong __init__ method của TelegramHandler
self.proxies = {
    'http': 'socks5://127.0.0.1:40000',   # WARP SOCKS5 proxy
    'https': 'socks5://127.0.0.1:40000'
}
```

## Cách 2: Sử dụng proxy khác

### Psiphon:
```python
self.proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}
```

### VPN Gate hoặc proxy miễn phí:
```python
self.proxies = {
    'http': 'http://proxy_ip:port',
    'https': 'http://proxy_ip:port'
}
```

## Cách 3: Thay đổi DNS

### Trong cmd (Run as Administrator):
```cmd
netsh interface ip set dns "Wi-Fi" static 1.1.1.1
netsh interface ip add dns "Wi-Fi" 1.0.0.1 index=2
```

### Hoặc thay đổi DNS trong Network Settings:
- Primary DNS: 1.1.1.1
- Secondary DNS: 1.0.0.1

## Test kết nối

Chạy script test:
```bash
python demo.py
```

Hoặc test riêng Telegram:
```python
from telegram_handler import TelegramHandler
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

telegram = TelegramHandler(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
print("Testing connection...")
result = telegram.test_connection()
print(f"Result: {result}")
```

## Debug các lỗi thường gặp

### Lỗi timeout:
- Tăng timeout trong `telegram_handler.py`:
```python
self.timeout = 60  # Tăng từ 30 lên 60 giây
```

### Lỗi SSL:
```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Thêm verify=False vào requests
response = requests.post(url, data=data, verify=False)
```

### Lỗi proxy:
- Kiểm tra proxy đang hoạt động
- Thử các port khác: 1080, 8080, 3128
- Disable proxy tạm thời: `self.proxies = None`

## Kiểm tra kết nối thủ công

Mở cmd và test:
```cmd
curl -x socks5://127.0.0.1:40000 https://api.telegram.org/bot<TOKEN>/getMe
```

Thay `<TOKEN>` bằng bot token thực của bạn.

---

**Lưu ý**: Nếu tất cả đều thất bại, hãy thử chạy hệ thống mà không gửi Telegram. Hệ thống vẫn sẽ ghi log và hiển thị cảnh báo trên màn hình.
