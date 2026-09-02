import os
import logging
from aiogram import Bot, Dispatcher, executor

from handlers import (
    start_command_answer,
    handle_city_message,
    Get_ob_havo_callback,
    incoming_message_autoreply,
    away_command,
    back_command,
    setphone_command,
    status_command,
)


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("Error: BOT_TOKEN environment variable is not set.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Register handlers
dp.register_message_handler(start_command_answer, commands=["start"])
dp.register_callback_query_handler(Get_ob_havo_callback)
dp.register_message_handler(handle_city_message, content_types=["text"])  # city names

# Auto-reply/forward handler (runs for many content types)
dp.register_message_handler(
    incoming_message_autoreply,
    content_types=["text", "photo", "video", "sticker", "audio", "voice", "document"],
)

# Owner commands
dp.register_message_handler(away_command, commands=["away"]) 
dp.register_message_handler(back_command, commands=["back"]) 
dp.register_message_handler(setphone_command, commands=["setphone"]) 
dp.register_message_handler(status_command, commands=["status"]) 


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
