from aiogram import types
from aiogram.dispatcher import FSMContext
from create import bot, dp
from commands.get_keyboard import get_account_keyboard
from commands.task_actions import check_user_values, get_check_page_title, check_range
from commands.general import print_stud, ConfirmDeletion, read_user_values, write_user_values
from commands.get_menu import callback_check_authentication
from db.commands import select_students, select_applications, add_application
from keyboard import stud_application_ikb, student_task_show, del_stud_ikb, stud_application_ikb_2, student_data_ikb

application_values = read_user_values("application_values")


def get_students(f=None):
    """
    Функция возвращающая список студентов
    :return: Список студентов
    """

    all_students = select_students()
    applications = select_applications()
    pending_students_ids = [student.student_id for student in applications]
    if not f:
        return [s for s in all_students if s.telegram_id not in pending_students_ids]
    return [s for s in all_students if s.telegram_id in pending_students_ids]


def get_student_msg(callback, dict_name, dict_values, f=None):
    """
    Функция возвращает клавиатуру и информацию о задаче
    :param f:
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Клавиатура и информация о задаче
    """

    students = get_students(f)
    usr_id = str(callback.from_user.id)

    if not students:
        msg_text = 'В данный момент данных нет.\nЗагляните позже.'
        return get_account_keyboard(usr_id), msg_text

    button = callback.data
    dict_values = check_user_values(usr_id, dict_name, dict_values)
    result = get_check_page_title(callback, dict_name, dict_values, len(students))
    msg_text, dict_values = result
    write_user_values(dict_name, dict_values)
    current_application = students[dict_values[usr_id]]
    msg_text += print_stud(current_application, button)

    if "application" in button:
        return stud_application_ikb, msg_text
    return student_data_ikb, msg_text


@dp.callback_query_handler(text=['show_students', "students_left", "students_right"])
@callback_check_authentication
async def show_students(callback: types.CallbackQuery):
    """
    Функция просмотра студентов.
    """

    keyboard, msg_text = get_student_msg(callback, "application_values", application_values, 1)
    await callback.message.edit_text(msg_text, reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(text=['show_applications', 'right_application', 'left_application'])
@callback_check_authentication
async def show_applications(callback: types.CallbackQuery):
    """
    Функция просмотра, отклонения/одобрения нерассмотренных заявок студентов.
    """

    keyboard, msg_text = get_student_msg(callback, "application_values", application_values)
    await callback.message.edit_text(msg_text, reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(text='approve')
@callback_check_authentication
async def approve_student(callback: types.CallbackQuery):
    """
    Функция одобрения заявки студента.
    """

    usr_id = str(callback.from_user.id)
    applications = get_students()
    student_id = applications[application_values[usr_id]].telegram_id
    add_application(student_id, callback.from_user.id, 1)
    application_values[usr_id] -= 1
    write_user_values("application_values", application_values)

    msg_text = ('Ваша заявка была <b>одобрена</b>.\nВы можете выбрать задачу из списка доступных задач.\n'
                'Чат для связи доступен по <a href="https://t.me/+FShhqiWUDJRjODky">этой ссылке</a>')

    await callback.message.edit_text('Заявка одобрена.', reply_markup=stud_application_ikb_2)
    await bot.send_message(student_id, msg_text, reply_markup=student_task_show,
                           parse_mode='HTML', disable_web_page_preview=True)


@dp.callback_query_handler(text='reject')
@callback_check_authentication
async def reject_student(callback: types.CallbackQuery):
    """
    Функция подтверждения отклонения заявки.
    """

    await callback.message.edit_text('Отклонить заявку?', reply_markup=del_stud_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='reject_yes', state=ConfirmDeletion.delete)
@callback_check_authentication
async def reject_student_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция отклонения заявки.
    """

    await state.update_data(delete=callback.data)
    usr_id = str(callback.from_user.id)
    applications = get_students()
    student_id = applications[application_values[usr_id]].telegram_id
    add_application(student_id, usr_id, 0)
    applications = get_students()
    check_range(len(applications), usr_id, "application_values", application_values)

    await state.finish()
    await bot.send_message(student_id, 'Ваша заявка была <b>отклонена</b>.', parse_mode='HTML')
    await callback.message.edit_text('Заявка отклонена.', reply_markup=stud_application_ikb_2)
