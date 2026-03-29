from aiogram import Bot, Dispatcher
from aiogram.types import Message,BotCommand
from asyncio import run
from aiogram.filters import Command, CommandStart
from handlers import start_command_answer,Get_ob_havo



dp = Dispatcher()

token = "8564972912:AAHcvJRgvVdJyx6ZHfLjVQP40APJTUGMO3I"

async def start_answer(bot: Bot):
    await bot.send_message(chat_id=1777869757, text="Bot ishga tushdi✅")

async def shutdown_answer(bot: Bot):
    await bot.send_message(chat_id=1777869757, text="Bot ish faoliyatidan to'xtadi❌")

async def start():

    dp.startup.register(start_answer)
    dp.message.register(start_command_answer, CommandStart())
    dp.callback_query.register(Get_ob_havo)
    dp.shutdown.register(shutdown_answer)

    bot = Bot(token)

    

    await dp.start_polling(bot, polling_timeout=1)


run(start())
