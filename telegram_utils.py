from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv  # <- Thêm dòng này

load_dotenv()  # <- Nạp biến môi trường từ file .env

async def send_telegram(photo_path="alert.png"):
    try:
        my_token = os.getenv("TELEGRAM_BOT_TOKEN")  # <- Dùng os.getenv()
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        bot = Bot(token=my_token)
        with open(photo_path, "rb") as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo, caption="Có xâm nhập, nguy hiểm!")
    except Exception as ex:
        print("Không thể gửi Telegram:", ex)
    else:
        print("Gửi thành công")
