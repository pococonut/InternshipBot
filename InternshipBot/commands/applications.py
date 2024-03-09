from aiogram import types
from aiogram.dispatcher import FSMContext
from create import bot, dp
from commands.general import print_stud, ConfirmDeletion, navigation, read_user_values, write_user_values
from db.commands import select_students, select_applications, add_application
from keyboard import admin_ikb, stud_application_ikb, student_task_show, del_stud_ikb, stud_application_ikb_2

application_values = read_user_values("application_values")


def get_pending_students():
    """
    Функция, возвращающая нерассмотренные заявки студентов и их количество.
    :return: Количество нерассмотренных заявок, нерассмотренные заявки.
    """

    all_students = select_students()
    applications = select_applications()
    pending_students_ids = [student.student_id for student in applications]
    pending_students = [s for s in all_students if s.telegram_id not in pending_students_ids]
    return pending_students


@dp.callback_query_handler(text='show_students')
async def show_applications(callback: types.CallbackQuery):
    """
    Функция просмотра, отклонения/одобрения нерассмотренных заявок студентов.
    """

    applications = get_pending_students()
    if not applications:
        msg_text = 'В данный момент заявок нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=admin_ikb)
        await callback.answer()
        return

    usr_id = str(callback.from_user.id)
    if usr_id not in application_values:
        application_values[usr_id] = 0
        write_user_values("application_values", application_values)

    count_students = len(applications)
    current_page = application_values[usr_id] + 1
    current_application = applications[application_values[usr_id]]
    page_string = f"<b>№</b> {current_page}/{count_students}\n\n"
    msg_text = page_string + print_stud(current_application, callback.data)
    await callback.message.edit_text(msg_text, reply_markup=stud_application_ikb, parse_mode='HTML')


@dp.callback_query_handler(text=['right_stud', 'left_stud'])
async def show_applications_lr(callback: types.CallbackQuery):
    """
    Функция просмотра, отклонения/одобрения нерассмотренных заявок студентов.
    """

    applications = get_pending_students()
    if not applications:
        msg_text = 'В данный момент заявок нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=admin_ikb)
        await callback.answer()
        return

    usr_id = str(callback.from_user.id)
    if usr_id not in application_values:
        application_values[usr_id] = 0
        write_user_values("application_values", application_values)

    count_students = len(applications)
    page_string, application_values[usr_id] = navigation(callback.data, application_values[usr_id], count_students)
    write_user_values("application_values", application_values)
    current_application = applications[application_values[usr_id]]
    msg_text = page_string + print_stud(current_application, callback.data)
    await callback.message.edit_text(msg_text, reply_markup=stud_application_ikb, parse_mode='HTML')


@dp.callback_query_handler(text='approve')
async def approve_student(callback: types.CallbackQuery):
    """
    Функция одобрения заявки студента.
    """

    usr_id = str(callback.from_user.id)
    applications = get_pending_students()
    student_id = applications[application_values[usr_id]].telegram_id
    add_application(student_id, callback.from_user.id, 1)
    application_values[usr_id] -= 1
    write_user_values("application_values", application_values)

    msg_text = ('Ваша заявка была <b>одобрена</b>.\n Вы можете выбрать задачу из списка доступных задач.\n'
                'Чат для связи доступен по <a href="https://t.me/+FShhqiWUDJRjODky">этой ссылке</a>')

    await callback.message.edit_text('Заявка одобрена.', reply_markup=stud_application_ikb_2)
    await bot.send_message(student_id, msg_text, reply_markup=student_task_show,
                           parse_mode='HTML', disable_web_page_preview=True)


@dp.callback_query_handler(text='reject')
async def reject_student(callback: types.CallbackQuery):
    """
    Функция подтверждения отклонения заявки.
    """

    await callback.message.edit_text('Отклонить заявку?', parse_mode='HTML', reply_markup=del_stud_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='reject_yes', state=ConfirmDeletion.delete)
async def reject_student_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция отклонения заявки.
    """

    await state.update_data(delete=callback.data)
    usr_id = str(callback.from_user.id)
    applications = get_pending_students()
    student_id = applications[application_values[usr_id]].telegram_id
    add_application(student_id, callback.from_user.id, 0)
    applications = get_pending_students()
    count_students = len(applications)

    condition1 = application_values[usr_id] >= count_students
    condition2 = application_values[usr_id] < count_students
    if count_students and (condition1 or condition2):
        application_values[usr_id] = 0
        write_user_values("application_values", application_values)

    await state.finish()
    await bot.send_message(student_id, 'Ваша заявка была <b>отклонена</b>.', parse_mode='HTML')
    await callback.message.edit_text('Заявка отклонена.', reply_markup=stud_application_ikb_2)
