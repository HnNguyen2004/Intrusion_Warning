"""
Script để lấy Chat ID chính xác
"""

import requests
from config import TELEGRAM_BOT_TOKEN

def get_chat_id():
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    
    print("📱 Hướng dẫn lấy Chat ID:")
    print("1. Gửi tin nhắn bất kỳ cho bot @Intrusion_Warning")
    print("2. Chạy script này để lấy Chat ID")
    print("\n🔍 Đang lấy updates...")
    
    try:
        response = requests.get(f"{base_url}/getUpdates", timeout=10, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok') and data.get('result'):
                updates = data['result']
                print(f"\n✅ Tìm thấy {len(updates)} tin nhắn:")
                
                for update in updates:
                    message = update.get('message', {})
                    chat = message.get('chat', {})
                    from_user = message.get('from', {})
                    text = message.get('text', '')
                    
                    chat_id = chat.get('id')
                    chat_type = chat.get('type')
                    first_name = from_user.get('first_name', 'Unknown')
                    username = from_user.get('username', 'No username')
                    
                    print(f"\n📝 Update ID: {update.get('update_id')}")
                    print(f"👤 From: {first_name} (@{username})")
                    print(f"💬 Chat ID: {chat_id}")
                    print(f"📂 Chat Type: {chat_type}")
                    print(f"✉️  Message: {text[:50]}...")
                    print("="*50)
                
                if updates:
                    latest_chat_id = updates[-1]['message']['chat']['id']
                    print(f"\n🎯 CHAT ID MỚI NHẤT: {latest_chat_id}")
                    print(f"\nThay đổi trong config.py:")
                    print(f'TELEGRAM_CHAT_ID = "{latest_chat_id}"')
                else:
                    print("\n❌ Không có tin nhắn nào. Hãy gửi tin nhắn cho bot trước!")
                    
            else:
                print(f"❌ API Error: {data.get('description', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    get_chat_id()
