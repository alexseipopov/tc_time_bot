from time import time
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *
from crud import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(mess: types.Message):
    if not select("admin", where={"tg_id": mess.from_user.id}):
        insert("admin", {"tg_id": mess.from_user.id})
    await mess.answer("Спасибо что нашли нас, тут тест")


@dp.message_handler(commands=["start_work"])
async def start_work(mess: types.Message):
    update("worker", {"time_delta": int(time()), "time_day": 0}, {"tg_id": mess.from_user.id})
    worker_name, worker_time_delta = select("worker", ["name", "time_delta"], where={"tg_id": mess.from_user.id})
    t = datetime.fromtimestamp(worker_time_delta)
    await bot.send_message(580045437, f"Сотрудник {worker_name} приступил к работе в {t.hour:02}:{t.minute:02}:{t.second:02}")
    await mess.answer("Удачного дня!. Время начала работы принято. Всё получится!!")
    

@dp.message_handler(commands=["break"])
async def _break(mess: types.Message):
    worker_name, worker_time_delta, worker_time_day = select("worker", ["name", "time_delta", "time_day"], where={"tg_id": mess.from_user.id})
    time_del = time() - worker_time_delta
    update("worker", {"time_day": worker_time_day + time_del}, {"tg_id": mess.from_user.id})
    t = datetime.fromtimestamp(worker_time_delta)
    current = datetime.fromtimestamp(time())
    await bot.send_message(580045437, f"Сотрудник {worker_name} отошел на перерыв в {current.hour:02}:{current.minute:02}:{current.second:02}")
    await mess.answer("Время работы остановлено")


@dp.message_handler(commands=["finish_break"])
async def finish_break(mess: types.Message):
    time_del = time() - select("worker", ["time_delta"], {"tg_id": mess.from_user.id})[0]
    worker_name, worker_time_delta = select("worker", ["name", "time_delta"], where={"tg_id": mess.from_user.id})
    t = datetime.fromtimestamp(worker_time_delta)
    current = datetime.fromtimestamp(time())
    update("worker", {"time_delta": int(time())}, {"tg_id": mess.from_user.id})
    await bot.send_message(580045437, f"Сотрудник {worker_name} вернулся с перерыва в {current.hour:02}:{current.minute:02}:{current.second:02}")
    await mess.answer("Время восстановлено")


@dp.message_handler(commands=["finish"])
async def finish_break(mess: types.Message):
    worker_name, worker_time_delta, worker_time_day = select("worker", ["name", "time_delta", "time_day"], where={"tg_id": mess.from_user.id})
    time_del = time() - worker_time_delta
    t = datetime.fromtimestamp(worker_time_delta)
    final_time = worker_time_day + time_del
    current = datetime.fromtimestamp(time())
    await bot.send_message(580045437, f"Сотрудник {worker_name} завершил работу в {current.hour:02}:{current.minute:02}:{current.second:02}, в общей сложности за день вышло: {int(final_time / (60 * 24)):02}:{int(final_time / (60 )):02}:{int(final_time % 60):02}")
    await mess.answer("Удачного дня, Спасибо!")


if __name__ == "__main__":
    executor.start_polling(dp)