from aiogram import types
from create import dp
from commands.general import get_keyboard, navigation, read_user_values, write_user_values, get_tasks_for_student, \
    short_long_task
from db.commands import select_task, select_already_get_stud, select_worker_task, get_user_type
from keyboard import task_ikb, student_task_already_choose, student_task_choose, task_without_del, task_worker_ikb, \
    task_worker_more_ikb, task_worker_more_without_del_ikb, task_student_more_ikb, task_worker_more_all, \
    task_worker_without_del, task_worker_own_ikb

tasks_values = read_user_values("tasks_values")


def get_keyboard_task(usr_id, have_task, task_id):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param usr_id: Идентификатор пользователя.
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :param task_id: Уникальный идентификатор пользователя в телеграм.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """

    usr_type = get_user_type(usr_id)[0]
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


def get_keyboard_more_task(usr_id, task_selected):
    """
    Функция получения клавиатуры в соответствии с типом пользователя при подробном просмотре задачи.
    :param usr_id: Идентификатор пользователя
    :param task_selected: Просматриваемая задача
    :return: Клавиатура
    """
    user_type = get_user_type(usr_id)[0]

    if user_type == 'student':
        return task_student_more_ikb
    if user_type == 'worker':
        return task_worker_more_all
    if task_selected:
        return task_worker_more_without_del_ikb
    return task_worker_more_ikb


def get_worker_own_keyboard(usr_id):
    """
    Функция возвращает клавиатуру в зависимости от того,
     закреплена ли задача за студентом или нет
    :param usr_id: Идентификатор пользователя
    :return: Клавиатура
    """

    if usr_id:
        return task_worker_without_del
    return task_worker_own_ikb


def get_tasks_for_user(usr_id, callback):

    user_type = get_user_type(usr_id)[0]
    if user_type == 'student':
        return get_tasks_for_student()
    elif 'worker' in callback:
        return select_worker_task(usr_id)
    else:
        return select_task()


def get_task_message_keyboard(usr_id, callback, dict_name, dict_values):
    """
    Функция возвращает клавиатуру и информацию о задаче
    :param usr_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Клавиатура и информация о задаче
    """

    tasks = get_tasks_for_user(usr_id, callback)

    if not tasks:
        keyboard = get_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        return keyboard, msg_text

    if usr_id not in dict_values:
        dict_values[usr_id] = 0
        write_user_values(f"{dict_name}", dict_values)

    count_tasks = len(tasks)

    condition1 = dict_values[usr_id] >= count_tasks
    if count_tasks and condition1:
        dict_values[usr_id] = count_tasks - 1
        write_user_values(f"{dict_name}", dict_values)

    current_task = tasks[dict_values[usr_id]]
    student_ids_task = current_task.student_id
    current_page = dict_values[usr_id]

    if 'worker' in callback:
        keyboard = get_worker_own_keyboard(current_task.student_id)
    else:
        keyboard = get_keyboard_task(usr_id, student_ids_task, usr_id)

    if 'right' not in callback and 'left' not in callback:
        if dict_values[usr_id] <= -1:
            current_page = count_tasks + dict_values[usr_id]
        msg_text = f"<b>№</b> {current_page + 1}/{count_tasks}\n\n" + short_long_task(current_task)
        return keyboard, msg_text

    s, dict_values[usr_id] = navigation(callback, current_page, count_tasks)
    write_user_values(dict_name, dict_values)
    current_task = tasks[dict_values[usr_id]]
    msg_text = s + short_long_task(current_task)
    return keyboard, msg_text


@dp.callback_query_handler(text=['show_task', 'right', 'left'])
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    usr_id = str(callback.from_user.id)
    keyboard, msg_text = get_task_message_keyboard(usr_id, callback.data, "tasks_values", tasks_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task')
async def show_more_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи.
    """

    usr_id = str(callback.from_user.id)
    tasks = get_tasks_for_user(usr_id, callback.data)

    current_task = tasks[tasks_values[usr_id]]
    task_selected = current_task.student_id
    keyboard = get_keyboard_more_task(usr_id, task_selected)
    msg_text = short_long_task(current_task, 1)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)

