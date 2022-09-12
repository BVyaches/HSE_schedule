from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
from sql_funcs import *
from main import *
from formats import *
from handlers.common import register_handlers_common
from handlers.user_work import register_handlers_user
bot = Bot(token='5752540390:AAHDFWdL4N1tY3I0PDWiBE90KdbW7NhsOr8')
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    register_handlers_common(dp)
    register_handlers_user(dp)
    await dp.start_polling()


async def auto_check():
    while True:
        print('Started')
        start_time = time.time()
        new_data = await check_sheets()
        active_users = await get_active_users()

        for sheet in new_data:
            for user in active_users:
                await bot.send_message(user, sheet)
                await bot.send_document(user, open(f'sheets/{sheet}.xls', 'rb'))
        print(time.time() - start_time)
        print('Stopped')
        await asyncio.sleep(600)

#asyncio.run(auto_check())
if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(main()),
             ioloop.create_task(auto_check()),
             ]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
