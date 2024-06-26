from aiogram import types

from create import dp
from db.commands import select_chosen_tasks, select_user
from commands.get_menu import callback_check_authentication
from commands.get_keyboard import get_account_keyboard
from commands.task_actions import check_user_values, get_check_page_title
from commands.general import print_stud, read_user_values, short_long_task
from keyboard import task_worker_stud, back_to_std

task_chosen_values = read_user_values("task_chosen_values")


def show_short_stud(s):
    """
    Функция вывода краткой информации о Студенте.
    :param s: Строка модели БД, относящаяся к конкретному студенту, с информацией о нем.
    :return: краткая информация о Студенте
    """

    v = f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n" \
        f"<b>Направление:</b> {s.specialties}\n" \
        f"<b>Курс:</b> {s.course}\n" \
        f"<b>Знания:</b> {s.knowledge}\n\n" \

    return v


def get_worker_chosen_task(callback, dict_name, dict_values):
    """
    Функция для получения информации о выбранных задачах сотрудника
    :param usr_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Информация о выбранных задачах сотрудника
    """

    usr_id = str(callback.from_user.id)
    tasks = select_chosen_tasks(usr_id)

    if not tasks:
        keyboard = get_account_keyboard(usr_id)
        return 'Ваши задачи еще не выбраны.', keyboard

    dict_values = check_user_values(usr_id, dict_name, dict_values)
    result = get_check_page_title(callback, dict_name, dict_values, len(tasks))
    msg_text, dict_values = result
    current_task = tasks[dict_values[usr_id]]
    student_id = current_task.student_id
    students_list = student_id.split()
    msg_text += f"👨‍🎓<b>Студент\ы</b>\n\n"

    if len(students_list) == 1:
        student = select_user(student_id)
        msg_text += show_short_stud(student)
    else:
        for student in students_list:
            msg_text += show_short_stud(select_user(student))

    msg_text += f"———————————————————\n\n"
    msg_text += f"📚<b>Выбранная задача</b>\n\n" + short_long_task(current_task)

    return msg_text, task_worker_stud


@dp.callback_query_handler(text=["worker_chosen_tasks", 'tws_right', 'tws_left'])
@callback_check_authentication
async def worker_chosen_t(callback: types.CallbackQuery):
    """
    Функция для просмотра выбранных студентами задач
    """

    msg_text, keyboard = get_worker_chosen_task(callback, "task_chosen_values", task_chosen_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='tws_student')
@callback_check_authentication
async def show_more_stud(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации о студенте.
    """

    usr_id = str(callback.from_user.id)
    chosen_task = select_chosen_tasks(usr_id)
    current_page = task_chosen_values[usr_id]
    students_ids = chosen_task[current_page].student_id
    students_list = students_ids.split()

    if len(students_list) == 1:
        student = select_user(chosen_task[current_page].student_id)
        msg_text = f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student)
    else:
        msg_text = ''
        for student_id in students_list:
            student = select_user(student_id)
            msg_text += f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student)
            if students_list[-1] != student_id:
                msg_text += "———————————————————\n\n"

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=back_to_std)
