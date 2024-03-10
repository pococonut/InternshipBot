from aiogram import types
from create import dp
from commands.general import get_keyboard, navigation, read_user_values, write_user_values, get_tasks_for_student, \
    short_long_task
from db.commands import user_type, select_task, select_already_get_stud, select_user
from keyboard import task_ikb, student_task_already_choose, student_task_choose, task_without_del, task_worker_ikb, \
    task_worker_more_ikb, task_worker_more_without_del_ikb, task_student_more_ikb, task_worker_more_all


tasks_values = read_user_values("tasks_values")


def get_keyboard_task(usr_type, have_task, task_id):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param usr_type: Тип пользователя (Студент, Администратор, Директор, Сотрудник).
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :param task_id: Уникальный идентификатор пользователя в телеграм.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """

    if usr_type == 'student':
        already_get = select_already_get_stud(task_id)
        if already_get:
            return student_task_already_choose
        return student_task_choose
    elif usr_type in ('admin', 'director') and have_task:
        return task_without_del
    elif usr_type == 'worker':
        return task_worker_ikb
    return task_ikb


def get_keyboard_more_task(usr_type, task_selected):
    """
    Функция получения клавиатуры в соответствии с типом пользователя при подробном просмотре задачи.
    :param usr_type: Тип пользователя
    :param task_selected: Просматриваемая задача
    :return: Клавиатура
    """

    if usr_type == 'student':
        return task_student_more_ikb
    if usr_type == 'worker':
        return task_worker_more_all
    if task_selected:
        return task_worker_more_without_del_ikb
    return task_worker_more_ikb


@dp.callback_query_handler(text='show_task')
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = get_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=keyboard)
        await callback.answer()
        return

    if usr_id not in tasks_values:
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    count_tasks = len(tasks)
    student_ids_task = tasks[tasks_values[usr_id]].student_id
    keyboard = get_keyboard_task(u_type, student_ids_task, usr_id)

    page = tasks_values[usr_id]
    if tasks_values[usr_id] <= -1:
        page = count_tasks + tasks_values[usr_id]

    current_task = tasks[tasks_values[usr_id]]
    msg_text = f"<b>№</b> {page + 1}/{count_tasks}\n\n" + short_long_task(current_task)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text=['right', 'left'])
async def show_task_lr(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = get_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=keyboard)
        await callback.answer()
        return

    if usr_id not in tasks_values:
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    count_tasks = len(tasks)
    student_ids_task = tasks[tasks_values[usr_id]].student_id
    keyboard = get_keyboard_task(u_type, student_ids_task, usr_id)

    current_page = tasks_values[usr_id]
    s, tasks_values[usr_id] = navigation(callback.data, current_page, count_tasks)
    write_user_values("tasks_values", tasks_values)

    current_task = tasks[tasks_values[usr_id]]
    msg_text = s + short_long_task(current_task)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task')
async def show_more_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    current_task = tasks[tasks_values[usr_id]]
    task_selected = current_task.student_id
    keyboard = get_keyboard_more_task(u_type, task_selected)
    msg_text = short_long_task(current_task, 1)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)

