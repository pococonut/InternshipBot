from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Новый пользователь", callback_data="new")
ib2 = InlineKeyboardButton(text="Изменнить данные", callback_data="change")
ib3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
ikb.add(ib1, ib2, ib3)

ikb2 = InlineKeyboardMarkup(row_width=2)
ib2_1 = InlineKeyboardButton(text="Начать регестрацию", callback_data="begin")
ib2_2 = InlineKeyboardButton(text="Вернуться", callback_data="return")
ikb2.add(ib2_1, ib2_2)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)
b1 = KeyboardButton(text="/help")
b2 = KeyboardButton(text="/description")
b3 = KeyboardButton(text="/registration")
b4 = KeyboardButton(text="/authorisation")

kb.add(b1).add(b2).add(b3).add(b4)