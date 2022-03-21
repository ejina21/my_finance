from aiogram import types

from my_bot.buttons import pay_buttons
from my_bot.init_bot import dp


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer(f'Приветствую, {msg.from_user.first_name}! Выберите необходимое действие, нажав на кнопку ниже.',
                     reply_markup=pay_buttons)
