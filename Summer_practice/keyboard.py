from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Новый пользователь", callback_data="new")
# ib2 = InlineKeyboardButton(text="Изменнить данные", callback_data="change")
ib3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
ikb.add(ib1, ib3)

ikb_2 = InlineKeyboardMarkup(row_width=2)
# ib2_1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
ib2_2 = InlineKeyboardButton(text="Просмотр стажировок", callback_data="intern_show")
ikb_2.add(ib2_2)

ikb_3 = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
ib1_3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
ib2_3 = InlineKeyboardButton(text="Просмотр стажировок", callback_data="intern_show")

ikb_3.add(ib1_3, ib2_3)

back_ikb = InlineKeyboardMarkup(row_width=2)
back_b = InlineKeyboardButton(text="Отменить действие", callback_data="back")
back_ikb.add(back_b)

back_cont_ikb = InlineKeyboardMarkup(row_width=2)
back_cont_b = InlineKeyboardButton(text="Начать регистрацию", callback_data="continue")
back_cont_ikb.add(back_b, back_cont_b)

admin_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_b1 = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
# admin_b2 = InlineKeyboardButton(text="Изменить задачу", callback_data="change_task")
# admin_b3 = InlineKeyboardButton(text="Удалить задачу", callback_data="del_task")
admin_b4 = InlineKeyboardButton(text="Просмотр задач", callback_data="show_task")
admin_b5 = InlineKeyboardButton(text="Просмотр заявок", callback_data="show_students")
admin_ikb.add(admin_b1).add(admin_b4).add(admin_b5)

task_ikb = InlineKeyboardMarkup(row_width=2)
task_b1 = InlineKeyboardButton(text="Изменить задачу", callback_data="change_task")
task_b2 = InlineKeyboardButton(text="Удалить задачу", callback_data="del_task")
task_b3 = InlineKeyboardButton(text="Дальше", callback_data="del_task")
task_ikb.add(task_b1, task_b2, task_b3)

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

change_ikb_2 = InlineKeyboardMarkup(row_width=2)
change_ib1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
change_ikb_2.add(change_ib1)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)

b1 = KeyboardButton(text="/help")
b2 = KeyboardButton(text="/description")
b3 = KeyboardButton(text="/registration")
b4 = KeyboardButton(text="/show")
b5 = KeyboardButton(text="/change")
b6 = KeyboardButton(text="/authorisation")

kb.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)