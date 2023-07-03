from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Новый пользователь", callback_data="new")
ib2 = InlineKeyboardButton(text="Изменнить данные", callback_data="change")
ib3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
ikb.add(ib1, ib2, ib3)

ikb2 = InlineKeyboardMarkup(row_width=2)
ib2_1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
ib2_2 = InlineKeyboardButton(text="Просмотр стажировок", callback_data="intern_show")
ikb2.add(ib2_1, ib2_2)


change_ikb = InlineKeyboardMarkup(row_width=2)
change_ib1 = InlineKeyboardButton(text="ФИО", callback_data="student_name")
change_ib2 = InlineKeyboardButton(text="ВУЗ", callback_data="university")
change_ib3 = InlineKeyboardButton(text="Факультет", callback_data="faculty")
change_ib4 = InlineKeyboardButton(text="Направление", callback_data="specialties")
change_ib5 = InlineKeyboardButton(text="Кафедра", callback_data="department")
change_ib6 = InlineKeyboardButton(text="Курс", callback_data="course")
change_ib7 = InlineKeyboardButton(text="Группа", callback_data="group")
change_ib8 = InlineKeyboardButton(text="Курсовые", callback_data="coursework")
change_ib9 = InlineKeyboardButton(text="Знания", callback_data="knowledge")
change_ikb.add(change_ib1, change_ib2, change_ib3, change_ib4, change_ib5, change_ib6, change_ib7, change_ib8, change_ib9)


kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)
b1 = KeyboardButton(text="/help")
b2 = KeyboardButton(text="/description")
b3 = KeyboardButton(text="/registration")
b4 = KeyboardButton(text="/authorisation")

kb.add(b1).add(b2).add(b3).add(b4)