from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from formats import main_keyboard
from sql_funcs import get_all_sheets, stop_status


async def send_sheets(message: types.Message):
    sheets = await get_all_sheets()
    await message.answer('Всё расписание с сайта:')
    for sheet in sheets:
        await message.answer_document(open(f'sheets/{sheet}.xls', 'rb'), caption=f'<b>{sheet}</b>', parse_mode='HTML')


async def stop_sending(message: types.Message):
    await stop_status(message.from_user.id)
    await message.answer('Рассылка остановлена, для восстановления отправьте /start')

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(send_sheets, Text(equals='Расписание',
                                                  ignore_case=True),
                                state='*')
    dp.register_message_handler(stop_sending, Text(equals='Остановить',
                                                  ignore_case=True),
                                state='*')
