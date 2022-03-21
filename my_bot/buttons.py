from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

PAY = 'Оплата'


button_pay = KeyboardButton(PAY)
pay_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pay_buttons.add(button_pay, )