from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from config import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(mess: types.Message):
    
    await mess.answer("Спасибо что нашли нас, тут тест")
