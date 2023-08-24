from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

new_user_ikb = InlineKeyboardMarkup(row_width=2)
new_user_ib1 = InlineKeyboardButton(text="Регистрация", callback_data="student")
new_user_ib2 = InlineKeyboardButton(text="Авторизация", callback_data="authorization")
new_user_ikb.add(new_user_ib1, new_user_ib2)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Новый пользователь", callback_data="new")
ib3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
ikb.add(ib1, ib3)

menu = InlineKeyboardButton(text="Меню", callback_data="menu")
chat = InlineKeyboardButton(text="Чат", callback_data="chat")

chat_ikb = InlineKeyboardMarkup(row_width=2)
chat_ikb.add(menu)


ikb_2 = InlineKeyboardMarkup(row_width=2)
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

# Клавиатура администратора
admin_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_b1 = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
admin_b4 = InlineKeyboardButton(text="Просмотр задач", callback_data="show_task")
admin_b5 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
admin_b6 = InlineKeyboardButton('Выбранные задачи', callback_data="worker_chosen_tasks")
admin_b7 = InlineKeyboardButton(text="Просмотр заявок", callback_data="show_students")
admin_b8 = InlineKeyboardButton(text="Добавить аккаунт", callback_data="add_user")
admin_b9 = InlineKeyboardButton(text="Просмотр аккаунтов", callback_data="show_add_user")
admin_b10 = InlineKeyboardButton(text="Экспорт данных", callback_data="export")
admin_ikb.add(admin_b1, admin_b4, admin_b5, admin_b6, admin_b7, admin_b8, admin_b9, admin_b10, chat)

# Навигация по добавленным аккаунтам
added_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
added_b1 = InlineKeyboardButton("Назад", callback_data="left_added")
added_b2 = InlineKeyboardButton("Вперед", callback_data="right_added")
added_b3 = InlineKeyboardButton("Удалить", callback_data="del_added")
added_ikb.add(added_b1,added_b2,added_b3).add(menu)

login_added_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
login_added_ikb.add(added_b1,added_b2).add(menu)

del_added_ikb = InlineKeyboardMarkup(row_width=2)
del_added_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_a_yes")
del_added_ikb.add(del_added_ib1, back_b)

back_added_ikb = InlineKeyboardMarkup(row_width=2)
back_added_b = InlineKeyboardButton("Вернуться", callback_data="show_add_user")
back_added_ikb.add(back_added_b)

# Добавить пользователя
add_usr = InlineKeyboardMarkup(row_width=2)
add_usr.add(admin_b8).add(menu)

# Экспорт данных
exp_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
exp_b1 = InlineKeyboardButton(text="Задачи", callback_data="exp_task")
exp_b2 = InlineKeyboardButton(text="Заявки", callback_data="exp_appl")
exp_b3 = InlineKeyboardButton(text="Сотрудники", callback_data="exp_worker")
exp_b4 = InlineKeyboardButton(text="Принятые студенты", callback_data="exp_approved")
exp_b5 = InlineKeyboardButton(text="Добавленные аккаунты", callback_data="exp_added")

exp_ikb.add(exp_b1, exp_b2, exp_b3, exp_b4, exp_b5).add(menu)


back_to_std = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_to_std_b1 = InlineKeyboardButton(text='Вернуться',  callback_data="worker_chosen_tasks")
back_to_std.add(back_to_std_b1)

admin_ikb2 = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_ikb2.add(ib1_3).add(admin_b1).add(admin_b4).add(admin_b5)

# Клавиатура сотрудника
worker_ikb = InlineKeyboardMarkup(row_width=2)
worker_b1 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
worker_ikb.add(admin_b1, admin_b4, worker_b1, admin_b6, chat)


stud_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
stud_ikb.add(ib1_3)

change_user_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
change_b1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
change_user_ikb.add(change_b1)
change_user_ikb.add(menu)

stud_appl_ikb = InlineKeyboardMarkup(row_width=2)
stud_appl_b1 = InlineKeyboardButton(text="Отклонить", callback_data="reject")
stud_appl_b2 = InlineKeyboardButton(text="Одобрить", callback_data="approve")
stud_appl_b4 = InlineKeyboardButton("Назад", callback_data="left_stud")
stud_appl_b5 = InlineKeyboardButton("Вперед", callback_data="right_stud")
stud_appl_ikb.add(stud_appl_b1, stud_appl_b2, stud_appl_b4, stud_appl_b5, menu)

stud_appl_ikb_2 = InlineKeyboardMarkup(row_width=2)
stud_appl_ikb_2.add(stud_appl_b4, stud_appl_b5)

stud_appl_back_ikb = InlineKeyboardMarkup(row_width=2)
stud_appl_back_b = InlineKeyboardButton("Вернуться", callback_data="show_students")
stud_appl_back_ikb.add(stud_appl_back_b)

task_rl_ikb = InlineKeyboardMarkup(row_width=2)
task_rl_b1 = InlineKeyboardButton("Назад", callback_data="left")
task_rl_b2 = InlineKeyboardButton("Вперед", callback_data="right")
task_rl_ikb.add(task_rl_b1, task_rl_b2)

# Клавиатура одобренного студента
stud_is_approve = InlineKeyboardMarkup(row_width=2)
stud_is_approve_b1 = InlineKeyboardButton('Выбранная задача', callback_data="stud_chosen_tasks")
stud_is_approve.add(ib1_3, ib2_3, admin_b4, stud_is_approve_b1, chat)

selected_task = InlineKeyboardMarkup(row_width=2)
selected_task.add(stud_is_approve_b1)

# студент
back_task_ikb = InlineKeyboardMarkup(row_width=2)
back_task_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="show_task")
back_task_ikb.add(stud_is_approve_b1).add(back_task_b).add(menu)

# работник
back_task_w_ikb = InlineKeyboardMarkup(row_width=2)
back_task_w_ikb.add(back_task_b).add(menu)

# работник - свои задачи
back_task_own_ikb = InlineKeyboardMarkup(row_width=2)
back_task_own_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="worker_task")
back_task_own_ikb.add(back_task_own_b).add(menu)

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
task_ikb.add(menu)

task_without_del = InlineKeyboardMarkup(row_width=2)
task_without_del.add(task_b0)
task_without_del.add(task_b1)
task_without_del.add(task_b4, task_b5)
task_without_del.add(menu)

task_worker_more_all = InlineKeyboardMarkup(row_width=2)
task_worker_more_all.add(back_task_b)

task_worker_more_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_ikb.add(task_b1, task_b2)
task_worker_more_ikb.add(back_task_b)

task_student_more_ikb = InlineKeyboardMarkup(row_width=2)
task_student_more_ikb.add(back_task_b)

task_worker_more_without_del_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_without_del_ikb.add(task_b1).add(back_task_b)

task_worker_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_ikb.add(task_b0)
task_worker_ikb.add(task_b4, task_b5)
task_worker_ikb.add(menu)

back_to_tasks_w = InlineKeyboardMarkup()
back_to_tasks_w_b1 = InlineKeyboardButton(text='Вернуться',  callback_data="worker_task")
back_to_tasks_w.add(back_to_tasks_w_b1)

stud_reject_task = InlineKeyboardMarkup(row_width=2)
stud_reject_task_b1 = InlineKeyboardButton('Отказаться от задачи', callback_data="reject_task")
stud_reject_task.add(stud_reject_task_b1)
stud_reject_task.add(menu)

reject_task_ikb = InlineKeyboardMarkup(row_width=2)
reject_task_b1 = InlineKeyboardButton(text="Отказаться", callback_data="reject_task_yes")
reject_task_ikb.add(reject_task_b1, back_b)

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
student_task_choose.add(menu)

student_task_already_choose = InlineKeyboardMarkup(row_width=2)
student_task_already_choose.add(task_b4, task_b5)
student_task_already_choose.add(student_task_choose_b1)
student_task_already_choose.add(menu)

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
task_worker_own_ikb.add(menu)

task_worker_more_w_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_w_ikb.add(task_worker_own_b3, task_worker_own_b4)
task_worker_more_w_ikb.add(back_to_tasks_w_b1)

task_worker_more_without_del_w_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_without_del_w_ikb.add(task_worker_own_b3).add(back_to_tasks_w_b1)

task_worker_without_del = InlineKeyboardMarkup(row_width=2)
task_worker_without_del_b1 = InlineKeyboardButton("Подробнее", callback_data="more_task_w")

task_worker_without_del.add(task_worker_without_del_b1)
task_worker_without_del.add(task_worker_own_b3)
task_worker_without_del.add(task_worker_own_b1, task_worker_own_b2)
task_worker_without_del.add(menu)

task_worker_stud = InlineKeyboardMarkup(row_width=2)
task_worker_stud_b1 = InlineKeyboardButton("Назад", callback_data="tws_left")
task_worker_stud_b2 = InlineKeyboardButton("Вперед", callback_data="tws_right")
task_worker_stud_b3 = InlineKeyboardButton("Студент", callback_data="tws_student")
task_worker_stud.add(task_worker_stud_b1, task_worker_stud_b2, task_worker_stud_b3)
task_worker_stud.add(menu)

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

del_task_worker_ikb = InlineKeyboardMarkup(row_width=2)
del_task_worker_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_w_yes")
del_task_worker_ikb.add(del_task_worker_ib1, back_b)

del_stud_ikb = InlineKeyboardMarkup(row_width=2)
del_stud_ib1 = InlineKeyboardButton(text="Отклонить", callback_data="reject_yes")
del_stud_ikb.add(del_stud_ib1, back_b)

change_ikb = InlineKeyboardMarkup(row_width=2)
change_ib1 = InlineKeyboardButton(text="ФИО", callback_data="student_name")
change_ib10 = InlineKeyboardButton(text="Номер телефона", callback_data="phone")
change_ib2 = InlineKeyboardButton(text="ВУЗ", callback_data="university")
change_ib3 = InlineKeyboardButton(text="Факультет", callback_data="faculty")
change_ib4 = InlineKeyboardButton(text="Направление", callback_data="specialties")
change_ib5 = InlineKeyboardButton(text="Кафедра", callback_data="department")
change_ib6 = InlineKeyboardButton(text="Курс", callback_data="course")
change_ib7 = InlineKeyboardButton(text="Группа", callback_data="group")
change_ib8 = InlineKeyboardButton(text="Курсовые", callback_data="coursework")
change_ib9 = InlineKeyboardButton(text="Знания", callback_data="knowledge")
change_ikb.add(change_ib1, change_ib10, change_ib2, change_ib3, change_ib4, change_ib5, change_ib6, change_ib7, change_ib8, change_ib9)
change_ikb.add(back_b)

change_worker_ikb = InlineKeyboardMarkup(row_width=2)
change_worker_ikb.add(change_ib1, change_ib10, back_b)

change_ikb_2 = InlineKeyboardMarkup(row_width=2)
change_ib1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
change_ikb_2.add(change_ib1)

# Пропустить шаг
skip_p = InlineKeyboardMarkup(row_width=2)
skip_ib1 = InlineKeyboardButton(text="Пропустить", callback_data="skip_phone")
skip_p.add(skip_ib1)

skip_n = InlineKeyboardMarkup(row_width=2)
skip_ib2 = InlineKeyboardButton(text="Пропустить", callback_data="skip_name")
skip_n.add(skip_ib2)

# Выбор типа пользователя
types_users = InlineKeyboardMarkup(row_width=2)
types_users_b1 = InlineKeyboardButton(text="Директор", callback_data="director")
types_users_b2 = InlineKeyboardButton(text="Администратор", callback_data="admin")
types_users_b3 = InlineKeyboardButton(text="Сотрудник", callback_data="worker")
types_users.add(types_users_b1).add(types_users_b2).add(types_users_b3)

# Повторить авторизацию
login_rep = InlineKeyboardMarkup(row_width=2)
lr_b1 = InlineKeyboardButton(text="Повторить авторизацию", callback_data="menu")
login_rep.add(lr_b1)

