from aiogram import types
from create import dp
from commands.general import navigation, read_user_values, write_user_values, get_tasks_for_student, short_long_task
from commands.get_menu import callback_check_authentication
from commands.get_keyboard import get_keyboard_more_task, get_keyboard_task, get_account_keyboard
from db.commands import select_task, select_already_get_stud, select_worker_task, get_user_type

tasks_values = read_user_values("tasks_values")


def get_tasks_for_user(usr_id, callback):
    """
    Функция для получения списка задач в зависимости от типа пользователя
    :param usr_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :return:
    """

    user_type = get_user_type(usr_id)[0]
    if callback == "more_task_student_chosen":
        task = select_already_get_stud(usr_id)
        if not task:
            return []
        return task
    if user_type == 'student':
        return get_tasks_for_student()
    elif 'worker' in callback:
        return select_worker_task(usr_id)
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
    if list != type(tasks):
        keyboard = get_keyboard_more_task(usr_id, tasks, callback)
        msg_text = short_long_task(tasks, 1)
        return keyboard, msg_text

    values = check_range(len(tasks), usr_id, dict_name, dict_values)[0]
    current_task = tasks[values[usr_id]]
    task_selected = current_task.student_id
    keyboard = get_keyboard_more_task(usr_id, task_selected, callback)
    msg_text = short_long_task(current_task, 1)
    return keyboard, msg_text


def get_check_page_title(callback, dict_name, dict_values, count_tasks):
    """
    Функция проверяющая текущий номер страницы и возвращающая заголовок навигации
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :param count_tasks: Количество задач
    :return: Заголовок навигации
    """

    usr_id = str(callback.from_user.id)
    button = callback.data

    if 'right' in button or 'left' in button:
        result = check_range(count_tasks, usr_id, dict_name, dict_values)
        dict_values = result[0]
        outside = result[1]
        page_title = f"<b>№</b> {count_tasks}/{count_tasks}\n\n"
        if outside:
            return page_title, dict_values

        current_page = dict_values[usr_id]
        result = navigation(button, current_page, count_tasks)
        page_title, dict_values[usr_id] = result
        write_user_values(dict_name, dict_values)
        return page_title, dict_values

    dict_values = check_range(count_tasks, usr_id, dict_name, dict_values)[0]
    current_page = dict_values[usr_id]
    if dict_values[usr_id] <= -1:
        current_page = count_tasks + dict_values[usr_id]
    page_title = f"<b>№</b> {current_page + 1}/{count_tasks}\n\n"
    return page_title, dict_values


def get_task_message_keyboard(callback, dict_name, dict_values):
    """
    Функция возвращает клавиатуру и информацию о задаче
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Клавиатура и информация о задаче
    """

    usr_id = str(callback.from_user.id)
    tasks = get_tasks_for_user(usr_id, callback)

    if not tasks:
        keyboard = get_account_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        return keyboard, msg_text

    dict_values = check_user_values(usr_id, dict_name, dict_values)
    result = get_check_page_title(callback, dict_name, dict_values, len(tasks))
    msg_text, dict_values = result
    write_user_values(dict_name, dict_values)

    current_task = tasks[dict_values[usr_id]]
    msg_text += short_long_task(current_task)

    students_id = current_task.student_id
    keyboard = get_keyboard_task(callback.data, usr_id, students_id)

    return keyboard, msg_text


@dp.callback_query_handler(text=['show_task', 'right', 'left'])
@callback_check_authentication
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    keyboard, msg_text = get_task_message_keyboard(callback, "tasks_values", tasks_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text=['more_task', 'more_task_student_chosen'])
@callback_check_authentication
async def show_more_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи.
    """

    keyboard, msg_text = get_task_more_message(callback, "tasks_values", tasks_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)



