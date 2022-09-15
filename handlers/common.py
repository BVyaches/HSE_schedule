from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from formats import main_keyboard
from sql_funcs import add_user


async def start_bot(message: types.Message):
    keyboard = await main_keyboard()
    await message.answer(
        'Hi')
    await add_user(message.from_user.id)
    await message.answer('Что будем делать?', reply_markup=keyboard)


async def cancel_operation(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = await main_keyboard()
    await message.answer('Вы отменили действие', reply_markup=keyboard)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*'),
    dp.register_message_handler(start_bot, Text(equals='Продолжить рассылку')),
    dp.register_message_handler(cancel_operation, commands='cancel', state='*')
    dp.register_message_handler(cancel_operation, Text(equals='Отмена',
                                                       ignore_case=True),
                                state='*')
