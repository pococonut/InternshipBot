from aiogram import types
from create import dp
from commands.general import get_keyboard, navigation, read_user_values, write_user_values, get_tasks_for_student, \
    short_long_task
from db.commands import select_task, select_already_get_stud, select_worker_task, get_user_type
from keyboard import task_ikb, student_task_already_choose, student_task_choose, task_without_del, task_worker_ikb, \
    task_worker_more_ikb, task_worker_more_without_del_ikb, task_student_more_ikb, task_worker_more_all, \
    task_worker_without_del, task_worker_own_ikb

tasks_values = read_user_values("tasks_values")


def get_keyboard_task(callback, usr_id, have_task):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param callback: Кнопка.
    :param usr_id: Идентификатор пользователя.
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """

    if 'worker' in callback:
        if have_task:
            return task_worker_without_del
        return task_worker_own_ikb

    usr_type = get_user_type(usr_id)[0]
    if usr_type == 'student':
        already_get = select_already_get_stud(usr_id)
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


def get_tasks_for_user(usr_id, callback):
    """
    Функция для получения списка задач в зависимости от типа пользователя
    :param usr_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :return:
    """

    user_type = get_user_type(usr_id)[0]
    if user_type == 'student':
        return get_tasks_for_student()
    elif 'worker' in callback:
        return select_worker_task(usr_id)
    else:
        return select_task()


def check_range(count_tasks, usr_id, dict_name, dict_values):
    """
    Функция для проверки на ошибку выхода из массива
    :param count_tasks: Количество задач
    :param usr_id: Идентификатор пользователя в телеграм
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Словарь навигации, флаг: True - выход за пределы массива, False - ошибки нет
    """

    flag = False
    condition_1 = abs(dict_values[usr_id]) >= count_tasks
    if count_tasks and condition_1:
        flag = True
        dict_values[usr_id] = count_tasks-1
        write_user_values(dict_name, dict_values)

    return dict_values, flag


def check_user_values(usr_id, dict_name, dict_values):
    """
    Функция для проверки наличия идентификатора пользователя в словаре навигации,
    если идентификатора пользователя нет, он записывается в словарь
    :param usr_id: Идентификатор пользователя в телеграм
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Словарь навигации
    """

    if usr_id not in dict_values:
        dict_values[usr_id] = 0
        write_user_values(dict_name, dict_values)
    return dict_values


def get_task_more_message(usr_id, callback, dict_name, dict_values):
    """
    Функция возвращает клавиатуру и информацию о задаче при подробном просмотре
    :param usr_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Клавиатура и информация о задаче
    """

    tasks = get_tasks_for_user(usr_id, callback)
    values = check_range(len(tasks), usr_id, dict_name, dict_values)[0]
    current_task = tasks[values[usr_id]]
    task_selected = current_task.student_id
    keyboard = get_keyboard_more_task(usr_id, task_selected)
    msg_text = short_long_task(current_task, 1)

    return keyboard, msg_text


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

    dict_values = check_user_values(usr_id, dict_name, dict_values)
    count_tasks = len(tasks)

    if 'right' in callback or 'left' in callback:
        result = check_range(count_tasks, usr_id, dict_name, dict_values)
        dict_values = result[0]
        outside = result[1]
        if outside:
            page_title = f"<b>№</b> {count_tasks}/{count_tasks}\n\n"
        else:
            current_page = dict_values[usr_id]
            result = navigation(callback, current_page, count_tasks)
            page_title = result[0]
            dict_values[usr_id] = result[1]
            write_user_values(dict_name, dict_values)
        msg_text = page_title
    else:
        dict_values = check_range(count_tasks, usr_id, dict_name, dict_values)[0]
        current_page = dict_values[usr_id]
        if dict_values[usr_id] <= -1:
            current_page = count_tasks + dict_values[usr_id]
        msg_text = f"<b>№</b> {current_page + 1}/{count_tasks}\n\n"

    current_task = tasks[dict_values[usr_id]]
    msg_text += short_long_task(current_task)
    students_id = current_task.student_id
    keyboard = get_keyboard_task(callback, usr_id, students_id)

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
    keyboard, msg_text = get_task_more_message(usr_id, callback.data, "tasks_values", tasks_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)



