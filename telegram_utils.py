from telegram import Bot
import asyncio

async def send_telegram(photo_path="alert.png"):
    try:
        my_token = "7803495830:AAFOIrci94vNMZGGcYoi2u9n4wFw8HjAwrA"
        bot = Bot(token=my_token)
        with open(photo_path, "rb") as photo:
            await bot.send_photo(chat_id="1823943673", photo=photo, caption="Có xâm nhập, nguy hiểm!")
    except Exception as ex:
        print("Không thể gửi Telegram:", ex)
    else:
        print("Gửi thành công")
