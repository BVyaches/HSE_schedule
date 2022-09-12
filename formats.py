
from aiogram import types


async def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Остановить', 'Расписание']
    keyboard.add(*buttons)
    return keyboard


async def stopped_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Продолжить рассылку']
    keyboard.add(*buttons)
    return keyboard

