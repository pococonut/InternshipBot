from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Кнопка с меню в зависимости от типа пользователя
menu = InlineKeyboardButton(text="Меню", callback_data="menu")

# Клавиатура для получения основного меню
chat_ikb = InlineKeyboardMarkup(row_width=2)
chat_ikb.add(menu)

# Клавиатура выбора между регистрацией и авторизацией для незарегистрированного пользователя
new_user_ikb = InlineKeyboardMarkup(row_width=2)
new_user_ib1 = InlineKeyboardButton(text="Регистрация", callback_data="student")
new_user_ib2 = InlineKeyboardButton(text="Авторизация", callback_data="authorization")
new_user_ikb.add(new_user_ib1, new_user_ib2)

# Клавиатура выбора типа пользователя
types_users = InlineKeyboardMarkup(row_width=2)
types_users_b1 = InlineKeyboardButton(text="Директор", callback_data="director")
types_users_b2 = InlineKeyboardButton(text="Администратор", callback_data="admin")
types_users_b3 = InlineKeyboardButton(text="Сотрудник", callback_data="worker")
types_users.add(types_users_b1).add(types_users_b2).add(types_users_b3)

# Клавиатура повтора авторизации
login_rep = InlineKeyboardMarkup(row_width=2)
lr_b1 = InlineKeyboardButton(text="Повторить авторизацию", callback_data="menu")
login_rep.add(lr_b1)

# Клавиатура администратора/директора
admin_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
admin_b1 = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
admin_b4 = InlineKeyboardButton(text="Просмотр задач", callback_data="show_task")
admin_b5 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
admin_b6 = InlineKeyboardButton('Выбранные задачи', callback_data="worker_chosen_tasks")
admin_b7 = InlineKeyboardButton(text="Просмотр заявок", callback_data="show_students")
admin_b8 = InlineKeyboardButton(text="Добавить аккаунт", callback_data="add_user")
admin_b9 = InlineKeyboardButton(text="Просмотр аккаунтов", callback_data="show_added_users")
admin_b10 = InlineKeyboardButton(text="Экспорт данных", callback_data="export")
chat = InlineKeyboardButton(text="Чат", callback_data="chat")
admin_ikb.add(admin_b1, admin_b4, admin_b5, admin_b6, admin_b7, admin_b8, admin_b9, admin_b10, chat)

# Клавиатура сотрудника
worker_ikb = InlineKeyboardMarkup(row_width=2)
worker_b1 = InlineKeyboardButton(text="Свои задачи", callback_data="worker_task")
worker_ikb.add(admin_b1, admin_b4, worker_b1, admin_b6, chat)

# Клавиатура не одобренного студента
student_not_approved = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
student_not_approved_b1 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
student_not_approved_b2 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
student_not_approved.add(student_not_approved_b1).add(student_not_approved_b2)

# Клавиатура одобренного студента
stud_is_approve = InlineKeyboardMarkup(row_width=2)
stud_is_approve_b1 = InlineKeyboardButton('Выбранная задача', callback_data="stud_chosen_tasks")
stud_is_approve_b2 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
stud_is_approve_b3 = InlineKeyboardButton(text="Просмотреть данные", callback_data="show")
stud_is_approve.add(stud_is_approve_b3, stud_is_approve_b2, admin_b4, stud_is_approve_b1, chat)

# Клавиатура отмены действия
back_ikb = InlineKeyboardMarkup(row_width=2)
back_b = InlineKeyboardButton(text="Отменить действие", callback_data="back")
back_ikb.add(back_b)

# Клавиатура продолжения/отмены регистрации
back_cont_ikb = InlineKeyboardMarkup(row_width=2)
back_cont_b = InlineKeyboardButton(text="Начать регистрацию", callback_data="continue")
back_cont_ikb.add(back_b, back_cont_b)

# Клавиатура продолжения/отмены добавления задачи
back_cont_task_ikb = InlineKeyboardMarkup(row_width=2)
back_cont_task_b = InlineKeyboardButton(text="Добавить задачу", callback_data="continue_task")
back_cont_task_ikb.add(back_b, back_cont_task_b)

# Кнопка отмены удаления аккаунта
back_added_before_del_b = InlineKeyboardButton(text="Отменить действие", callback_data="back_added")

# Клавиатура для возвращения к просмотру аккаунтов, после удаление аккаунта
back_added_ikb = InlineKeyboardMarkup(row_width=2)
back_added_after_del_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="show_added_users")
back_added_ikb.add(back_added_after_del_b).add(menu)

# Клавиатура для возвращения к просмотру выбранных задач (для сотрудников)
back_to_std = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_to_std_b1 = InlineKeyboardButton(text='Вернуться',  callback_data="worker_chosen_tasks")
back_to_std.add(back_to_std_b1)

# Клавиатура для студента, после выбора задачи
back_task_ikb = InlineKeyboardMarkup(row_width=2)
back_task_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="show_task")
back_task_ikb.add(stud_is_approve_b1).add(back_task_b).add(menu)

# Клавиатура для возвращения к просмотру задач
back_task_w_ikb = InlineKeyboardMarkup(row_width=2)
back_task_w_ikb.add(back_task_b).add(menu)

# Клавиатура для возвращения к просмотру задач сотрудника
back_task_own_ikb = InlineKeyboardMarkup(row_width=2)
back_task_own_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="worker_task")
back_task_own_ikb.add(back_task_own_b).add(menu)

# Клавиатура для студента, после выбора задачи
back_task_ikb = InlineKeyboardMarkup(row_width=2)
back_task_b = InlineKeyboardButton("Вернуться к просмотру", callback_data="show_task")
back_task_ikb.add(stud_is_approve_b1).add(back_task_b).add(menu)

# Клавиатура для возвращения к просмотру задач
back_task_w_ikb = InlineKeyboardMarkup(row_width=2)
back_task_w_ikb.add(back_task_b).add(menu)

# Клавиатура для возвращения к просмотру заявок сотрудника
back_applications = InlineKeyboardMarkup(row_width=2)
back_applications_b1 = InlineKeyboardButton(text="Вернуться к просмотру", callback_data="show_students")
back_applications.add(back_applications_b1).add(menu)

# Клавиатура навигации\удаления по добавленным аккаунтам
added_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
added_b1 = InlineKeyboardButton("Назад", callback_data="left_added")
added_b2 = InlineKeyboardButton("Вперед", callback_data="right_added")
added_b3 = InlineKeyboardButton("Удалить", callback_data="del_added")
added_ikb.add(added_b1,added_b2,added_b3).add(menu)

# Клавиатура исключающая удаление аккаунта, если пользователь авторизовался
login_added_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
login_added_ikb.add(added_b1, added_b2).add(menu)

# Клавиатура для добавления аккаунта
add_usr = InlineKeyboardMarkup(row_width=2)
add_usr.add(admin_b8).add(admin_b9).add(menu)

# Клавиатура для получения данных в виде excel-таблиц
exp_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
exp_b1 = InlineKeyboardButton(text="Задачи", callback_data="exp_task")
exp_b2 = InlineKeyboardButton(text="Заявки", callback_data="exp_appl")
exp_b3 = InlineKeyboardButton(text="Сотрудники", callback_data="exp_worker")
exp_b4 = InlineKeyboardButton(text="Принятые студенты", callback_data="exp_approved")
exp_b5 = InlineKeyboardButton(text="Добавленные аккаунты", callback_data="exp_added")
exp_ikb.add(exp_b1, exp_b2, exp_b3, exp_b4, exp_b5).add(menu)

# Клавиатура для просмотра данных студента
stud_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
stud_ikb.add(stud_is_approve_b3)

# Клавиатура для просмотра, отклонения/одобрения заявок студентов
stud_application_ikb = InlineKeyboardMarkup(row_width=2)
stud_application_b1 = InlineKeyboardButton(text="Отклонить", callback_data="reject")
stud_application_b2 = InlineKeyboardButton(text="Одобрить", callback_data="approve")
stud_application_b4 = InlineKeyboardButton("Назад", callback_data="left_stud")
stud_application_b5 = InlineKeyboardButton("Вперед", callback_data="right_stud")
stud_application_ikb.add(stud_application_b1, stud_application_b2, stud_application_b4, stud_application_b5, menu)

# Клавиатура для просмотра заявок студентов
stud_application_ikb_2 = InlineKeyboardMarkup(row_width=2)
stud_application_ikb_2.add(stud_application_b4, stud_application_b5)

# Клавиатура для просмотра выбранной задачи
selected_task = InlineKeyboardMarkup(row_width=2)
selected_task.add(stud_is_approve_b1)

# Клавиатура для просмотра, изменения\удаления задач
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

# Клавиатура для просмотра задач
task_without_del = InlineKeyboardMarkup(row_width=2)
task_without_del.add(task_b0)
task_without_del.add(task_b1)
task_without_del.add(task_b4, task_b5)
task_without_del.add(menu)

# Клавиатура для подробного просмотра задачи
task_worker_more_all = InlineKeyboardMarkup(row_width=2)
task_worker_more_all.add(back_task_b)

# Клавиатура для подробного просмотра, удаления/редактирования задачи
task_worker_more_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_ikb.add(task_b1, task_b2)
task_worker_more_ikb.add(back_task_b)

# Клавиатура для подробного просмотра задачи (для студента)
task_student_more_ikb = InlineKeyboardMarkup(row_width=2)
task_student_more_ikb.add(back_task_b)

# Клавиатура для подробного просмотра, изменения задачи
task_worker_more_without_del_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_without_del_ikb.add(task_b1).add(back_task_b)

# Клавиатура для подробного просмотра задач (для сотрудника)
task_worker_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_ikb.add(task_b0)
task_worker_ikb.add(task_b4, task_b5)
task_worker_ikb.add(menu)

# Клавиатура для отказа от задачи (для студента)
stud_reject_task = InlineKeyboardMarkup(row_width=2)
stud_reject_task_b1 = InlineKeyboardButton('Отказаться от задачи', callback_data="reject_task")
stud_reject_task.add(stud_reject_task_b1)
stud_reject_task.add(menu)

# Клавиатура для подтверждения отказа от задачи (для студента)
reject_task_ikb = InlineKeyboardMarkup(row_width=2)
reject_task_b1 = InlineKeyboardButton(text="Отказаться", callback_data="reject_task_yes")
reject_task_ikb.add(reject_task_b1, back_b)

# Клавиатура для просмотра задач после одобрения заявки (для студента)
student_task_show = InlineKeyboardMarkup(row_width=2)
student_task_show.add(admin_b4)

# Клавиатура для просмотра выбранных студентами задач (для сотрудников)
task_is_approve = InlineKeyboardMarkup(row_width=2)
task_is_approve_b1 = InlineKeyboardButton('Выбранные задачи', callback_data="worker_chosen_tasks")
task_is_approve.add(task_is_approve_b1)

# Клавиатура для просмотра, выбора задач (для студентов)
student_task_choose = InlineKeyboardMarkup(row_width=2)
student_task_choose_b1 = InlineKeyboardButton("Подробнее", callback_data="more_task")
student_task_choose_b2 = InlineKeyboardButton("Выбрать", callback_data="stud_get_task")
student_task_choose.add(task_b4, task_b5)
student_task_choose.add(student_task_choose_b1)
student_task_choose.add(student_task_choose_b2)
student_task_choose.add(menu)

# Клавиатура для просмотра задач (для студентов)
student_task_already_choose = InlineKeyboardMarkup(row_width=2)
student_task_already_choose.add(task_b4, task_b5)
student_task_already_choose.add(student_task_choose_b1)
student_task_already_choose.add(menu)

# Клавиатура для просмотра, удаления\редактирования задач сотрудника (для сотрудников)
task_worker_own_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_own_b0 = InlineKeyboardButton("Подробнее", callback_data="more_task_worker")
task_worker_own_b1 = InlineKeyboardButton("Назад", callback_data="worker_left")
task_worker_own_b2 = InlineKeyboardButton("Вперед", callback_data="worker_right")
task_worker_own_b3 = InlineKeyboardButton(text="Изменить", callback_data="change_task_worker")
task_worker_own_b4 = InlineKeyboardButton(text="Удалить", callback_data="del_task_worker")
task_worker_own_ikb.add(task_worker_own_b0)
task_worker_own_ikb.add(task_worker_own_b3, task_worker_own_b4, task_worker_own_b1, task_worker_own_b2)
task_worker_own_ikb.add(menu)

# Клавиатура для удаления\редактирования задачи сотрудника (для сотрудников)
task_worker_more_w_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_w_ikb.add(task_worker_own_b3, task_worker_own_b4)
task_worker_more_w_ikb.add(admin_b5)

# Клавиатура для редактирования задачи сотрудника (для сотрудников)
task_worker_more_without_del_w_ikb = InlineKeyboardMarkup(row_width=2)
task_worker_more_without_del_w_ikb.add(task_worker_own_b3).add(admin_b5)

# Клавиатура для просмотра, редактирования задач сотрудника (для сотрудников)
task_worker_without_del = InlineKeyboardMarkup(row_width=2)
task_worker_without_del_b1 = InlineKeyboardButton("Подробнее", callback_data="more_task_worker")
task_worker_without_del.add(task_worker_without_del_b1)
task_worker_without_del.add(task_worker_own_b3)
task_worker_without_del.add(task_worker_own_b1, task_worker_own_b2)
task_worker_without_del.add(menu)

# Клавиатура для просмотра выбранных студентами задач сотрудника и информации о студентах (для сотрудников)
task_worker_stud = InlineKeyboardMarkup(row_width=2)
task_worker_stud_b1 = InlineKeyboardButton("Назад", callback_data="tws_left")
task_worker_stud_b2 = InlineKeyboardButton("Вперед", callback_data="tws_right")
task_worker_stud_b3 = InlineKeyboardButton("Студент", callback_data="tws_student")
task_worker_stud.add(task_worker_stud_b1, task_worker_stud_b2, task_worker_stud_b3)
task_worker_stud.add(menu)

# Клавиатура для изменения данных студента
change_user_ikb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
change_b1 = InlineKeyboardButton(text="Изменить данные", callback_data="change")
change_user_ikb.add(change_b1)
change_user_ikb.add(menu)

# Клавиатура для изменения параметров задачи (для сотрудников)
change_task_ikb = InlineKeyboardMarkup(row_width=2)
change_task_b1 = InlineKeyboardButton(text="Название", callback_data="change_task_name")
change_task_b2 = InlineKeyboardButton(text="Цель", callback_data="change_task_goal")
change_task_b3 = InlineKeyboardButton(text="Описание", callback_data="change_task_description")
change_task_b4 = InlineKeyboardButton(text="Задачи", callback_data="change_task_tasks")
change_task_b5 = InlineKeyboardButton(text="Навыки и технологии", callback_data="change_task_technologies")
change_task_b6 = InlineKeyboardButton(text="Получаемые навыки", callback_data="change_task_new_skills")
change_task_b7 = InlineKeyboardButton("Кол-во людей", callback_data="change_num_people")
change_task_b8 = InlineKeyboardButton("Материалы", callback_data="change_materials")
change_task_back = InlineKeyboardButton("Отменить действие", callback_data="back_change_tasks")
change_task_ikb.add(change_task_b1, change_task_b2, change_task_b3, change_task_b4, change_task_b5, change_task_b6, change_task_b7, change_task_b8)
change_task_ikb.add(change_task_back)

# Клавиатура для изменения параметров заявки (для студентов)
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

# Клавиатура для изменения личных данных (для сотрудников)
change_worker_ikb = InlineKeyboardMarkup(row_width=2)
change_worker_ikb.add(change_ib1, change_ib10, back_b)

# Клавиатура для подтверждения действия удаление аккаунта
del_added_ikb = InlineKeyboardMarkup(row_width=2)
del_added_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_a_yes")
del_added_ikb.add(del_added_ib1, back_added_before_del_b)

# Клавиатура для удаления задачи (для сотрудников)
del_task_ikb = InlineKeyboardMarkup(row_width=2)
del_task_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_yes")
del_task_ib2 = InlineKeyboardButton(text="Отменить действие", callback_data="back_tasks")
del_task_ikb.add(del_task_ib1, del_task_ib2)

# Клавиатура для удаления задачи сотрудника(для сотрудников)
del_task_worker_ikb = InlineKeyboardMarkup(row_width=2)
del_task_worker_ib1 = InlineKeyboardButton(text="Удалить", callback_data="del_yes_worker")
del_task_worker_ikb.add(del_task_worker_ib1, back_b)

# Клавиатура для отклонения заявки студента (для администратора\директора)
del_stud_ikb = InlineKeyboardMarkup(row_width=2)
del_stud_ib1 = InlineKeyboardButton(text="Отклонить", callback_data="reject_yes")
del_stud_ib2 = InlineKeyboardButton(text="Отменить действие", callback_data="back_application")
del_stud_ikb.add(del_stud_ib1, del_stud_ib2)