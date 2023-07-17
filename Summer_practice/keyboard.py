from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
ib2_3 = InlineKeyboardButton(text="Изменить данные", callback_data="change")

ikb_3.add(ib1_3).add(ib2_3)

back_ikb = InlineKeyboardMarkup(row_width=2)
back_b = InlineKeyboardButton(text="Отменить действие", callback_data="back")
back_ikb.add(back_b)

back_cont_ikb = InlineKeyboardMarkup(row_width=2)
back_cont_b = InlineKeyboardButton(text="Начать регистрацию", callback_data="continue")
back_cont_ikb.add(back_b, back_cont_b)

back_cont_task_ikb = InlineKeyboardMarkup(row_width=2)
back_cont_task_b = InlineKeyboardButton(text="Добавить задачу", callback_data="continue_task")
back_cont_task_ikb.add(back_b, back_cont_task_b)


admin_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_b1 = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
admin_b4 = InlineKeyboardButton(text="Просмотр задач", callback_data="show_task")
admin_b5 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
admin_b6 = InlineKeyboardButton('Выбранные задачи', callback_data="worker_chosen_tasks")
admin_b7 = InlineKeyboardButton(text="Просмотр заявок", callback_data="show_students")

admin_ikb.add(admin_b1, admin_b4, admin_b5, admin_b6, admin_b7)

back_to_std = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_to_std_b1 = InlineKeyboardButton(text='Вернуться',  callback_data="worker_chosen_tasks")
back_to_std.add(back_to_std_b1)

admin_ikb2 = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_ikb2.add(ib1_3).add(admin_b1).add(admin_b4).add(admin_b5)

worker_ikb = InlineKeyboardMarkup(row_width=2)
worker_b1 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
worker_ikb.add(admin_b1).add(admin_b4).add(worker_b1).add(admin_b6)


stud_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
stud_ikb.add(ib1_3)

change_stud_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
change_stud_b1 = InlineKeyboardButton(text="Изменнить данные", callback_data="change")
change_stud_ikb.add(change_stud_b1)

stud_appl_ikb = InlineKeyboardMarkup(row_width=2)
stud_appl_b1 = InlineKeyboardButton(text="Отклонить", callback_data="reject")
stud_appl_b2 = InlineKeyboardButton(text="Одобрить", callback_data="approve")
stud_appl_b4 = InlineKeyboardButton("Назад", callback_data="left_stud")
stud_appl_b5 = InlineKeyboardButton("Вперед", callback_data="right_stud")
stud_appl_ikb.add(stud_appl_b1, stud_appl_b2, stud_appl_b4, stud_appl_b5)

stud_appl_ikb_2 = InlineKeyboardMarkup(row_width=2)
stud_appl_ikb_2.add(stud_appl_b4, stud_appl_b5)

stud_appl_back_ikb = InlineKeyboardMarkup(row_width=2)
stud_appl_back_b = InlineKeyboardButton("Вернуться", callback_data="show_students")
stud_appl_back_ikb.add(stud_appl_back_b)

task_rl_ikb = InlineKeyboardMarkup(row_width=2)
task_rl_b1 = InlineKeyboardButton("Назад", callback_data="left")
task_rl_b2 = InlineKeyboardButton("Вперед", callback_data="right")
task_rl_ikb.add(task_rl_b1, task_rl_b2)

back_task_ikb = InlineKeyboardMarkup(row_width=2)
back_task_b = InlineKeyboardButton("Вернуться", callback_data="show_task")
back_task_ikb.add(back_task_b)

task_rlw_ikb = InlineKeyboardMarkup(row_width=2)
task_rlw_b1 = InlineKeyboardButton("Назад", callback_data="worker_left")
task_rlw_b2 = InlineKeyboardButton("Вперед", callback_data="worker_right")
task_rlw_ikb.add(task_rlw_b1, task_rlw_b2)


task_ikb = InlineKeyboardMarkup(row_width=2)
task_b0 = InlineKeyboardButton("Подробнее", callback_data="more_task")
task_b1 = InlineKeyboardButton(text="Изменить", callback_data="change_task")
task_b2 = InlineKeyboardButton(text="Удалить", callback_data="del_task")
task_b4 = InlineKeyboardButton("Назад", callback_data="left")
task_b5 = InlineKeyboardButton("Вперед", callback_data="right")
task_ikb.add(task_b0)
task_ikb.add(task_b1, task_b2)
task_ikb.add(task_b4, task_b5)

task_without_del = InlineKeyboardMarkup(row_width=2)
task_without_del.add(task_b0)
task_without_del.add(task_b1)
task_without_del.add(task_b4, task_b5)


task_worker_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_ikb.add(task_b0)
task_worker_ikb.add(task_b4, task_b5)

back_to_tasks_w = InlineKeyboardMarkup()
back_to_tasks_w_b1 = InlineKeyboardButton(text='Вернуться',  callback_data="worker_task")
back_to_tasks_w.add(back_to_tasks_w_b1)

stud_is_approve = InlineKeyboardMarkup(row_width=2)
stud_is_approve_b1 = InlineKeyboardButton('Выбранная задача', callback_data="stud_chosen_tasks")
stud_is_approve.add(ib1_3, ib2_3, admin_b4, stud_is_approve_b1)

stud_reject_task = InlineKeyboardMarkup(row_width=2)
stud_reject_task_b1 = InlineKeyboardButton('Отказаться от задачи', callback_data="reject_task")
stud_reject_task.add(stud_reject_task_b1)

student_task_show = InlineKeyboardMarkup(row_width=2)
student_task_show.add(admin_b4)

task_is_approve = InlineKeyboardMarkup(row_width=2)
task_is_approve_b1 = InlineKeyboardButton('Выбранные задачи', callback_data="worker_chosen_tasks")
task_is_approve.add(task_is_approve_b1)

student_task_choose = InlineKeyboardMarkup(row_width=2)
student_task_choose_b1 = InlineKeyboardButton("Подробнее", callback_data="more_task")
student_task_choose_b2 = InlineKeyboardButton("Выбрать", callback_data="stud_get_task")
student_task_choose.add(task_b4, task_b5)
student_task_choose.add(student_task_choose_b1)
student_task_choose.add(student_task_choose_b2)

student_task_already_choose = InlineKeyboardMarkup(row_width=2)
student_task_already_choose.add(task_b4, task_b5)
student_task_already_choose.add(student_task_choose_b1)

student_task_choose_cont = InlineKeyboardMarkup(row_width=2)
student_task_choose_cont.add(task_b4, task_b5)

task_worker_own_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_own_b0 = InlineKeyboardButton("Подробнее", callback_data="more_task_w")
task_worker_own_b1 = InlineKeyboardButton("Назад", callback_data="worker_left")
task_worker_own_b2 = InlineKeyboardButton("Вперед", callback_data="worker_right")
task_worker_own_b3 = InlineKeyboardButton(text="Изменить", callback_data="change_task_w")
task_worker_own_b4 = InlineKeyboardButton(text="Удалить", callback_data="del_task_w")
task_worker_own_ikb.add(task_worker_own_b0)
task_worker_own_ikb.add(task_worker_own_b3, task_worker_own_b4, task_worker_own_b1, task_worker_own_b2)

task_worker_without_del = InlineKeyboardMarkup(row_width=2)
task_worker_without_del.add(task_b0)
task_worker_without_del.add(task_worker_own_b3)
task_worker_without_del.add(task_worker_own_b1, task_worker_own_b2)


task_worker_stud = InlineKeyboardMarkup(row_width=2)
task_worker_stud_b1 = InlineKeyboardButton("Назад", callback_data="tws_left")
task_worker_stud_b2 = InlineKeyboardButton("Вперед", callback_data="tws_right")
task_worker_stud_b3 = InlineKeyboardButton("Студент", callback_data="tws_student")
task_worker_stud.add(task_worker_stud_b1, task_worker_stud_b2, task_worker_stud_b3)


change_task_ikb = InlineKeyboardMarkup(row_width=2)
change_task_b1 = InlineKeyboardButton(text="Название", callback_data="change_task_name")
change_task_b2 = InlineKeyboardButton(text="Цель", callback_data="change_task_goal")
change_task_b3 = InlineKeyboardButton(text="Описание", callback_data="change_task_description")
change_task_b4 = InlineKeyboardButton(text="Задачи", callback_data="change_task_tasks")
change_task_b5 = InlineKeyboardButton(text="Навыки и технологии", callback_data="change_task_technologies")
change_task_b6 = InlineKeyboardButton(text="Получаемые навыки", callback_data="change_task_new_skills")
change_task_b7 = InlineKeyboardButton("Кол-во людей", callback_data="change_num_people")
change_task_b8 = InlineKeyboardButton("Материалы", callback_data="change_materials")
change_task_ikb.add(change_task_b1, change_task_b2, change_task_b3, change_task_b4, change_task_b5, change_task_b6, change_task_b7, change_task_b8)
change_task_ikb.add(back_b)

del_task_ikb = InlineKeyboardMarkup(row_width=2)
del_task_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_yes")
del_task_ikb.add(del_task_ib1, back_b)

del_stud_ikb = InlineKeyboardMarkup(row_width=2)
del_stud_ib1 = InlineKeyboardButton(text="Отклонить", callback_data="reject_yes")
del_stud_ikb.add(del_stud_ib1, back_b)

reject_task_ikb = InlineKeyboardMarkup(row_width=2)
reject_task_b1 = InlineKeyboardButton(text="Отказаться", callback_data="reg_task_yes")
reject_task_ikb.add(reject_task_b1, back_b)

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
change_ikb.add(back_b)

change_worker_ikb = InlineKeyboardMarkup(row_width=2)
change_worker_ikb.add(change_ib1)

change_ikb_2 = InlineKeyboardMarkup(row_width=2)
change_ib1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
change_ikb_2.add(change_ib1)