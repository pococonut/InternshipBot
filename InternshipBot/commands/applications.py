import logging
from aiogram import types
from create import bot, dp
from aiogram.dispatcher import FSMContext
from commands.general import print_stud, ConfirmDeletion, navigation, read_user_values, write_user_values
from db.commands import select_students, select_applications, add_application
from keyboard import admin_ikb, stud_application_ikb, student_task_show, del_stud_ikb, stud_application_ikb_2


globalDict = read_user_values("globalDict")


def count_get_students():
    """
    Функция, возвращающая нерассмотренные заявки студентов и их количество.
    :return: Количество нерассмотренных заявок, нерассмотренные заявки.
    """
    all_students = select_students()
    applications = select_applications()
    not_accepted_stud = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]

    count_student = None
    if not_accepted_stud:
        count_student = len(all_students) - len(applications)

    return count_student, not_accepted_stud


def current_student(page_s):
    """
    Функция получения id студента в телеграм для текущей заявки.
    :param page_s: Номер рассматриваемой заявки из списка всех заявок.
    :return:  Id студента в телеграм.
    """
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    student_id = students[page_s].telegram_id
    return student_id


@dp.callback_query_handler(text='show_students')
async def show_students(callback: types.CallbackQuery):
    """
    Функция просмотра, отклонения/одобрения нерассмотренных заявок студентов.
    """
    count_students, students = count_get_students()
    usr_id = str(callback.from_user.id)
    if usr_id not in globalDict:
        globalDict[usr_id] = 0
        write_user_values("globalDict", globalDict)

    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
        await callback.answer()
    else:
        count_students, students = count_get_students()
        await callback.message.edit_text(f"<b>№</b> {globalDict[usr_id] + 1}/{count_students}\n\n" +
                                         print_stud(students[globalDict[usr_id]], callback.data),
                                         reply_markup=stud_application_ikb, parse_mode='HTML')


@dp.callback_query_handler(text=['right_stud', 'left_stud'])
async def show_students_lr(callback: types.CallbackQuery):
    """
    Функция просмотра, отклонения/одобрения нерассмотренных заявок студентов.
    """
    count_students, students = count_get_students()
    usr_id = str(callback.from_user.id)
    if usr_id not in globalDict:
        globalDict[usr_id] = 0
        write_user_values("globalDict", globalDict)

    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
        await callback.answer()
    else:
        s, globalDict[usr_id] = navigation(callback.data, globalDict[usr_id], count_students)
        write_user_values("globalDict", globalDict)
        await callback.message.edit_text(s + print_stud(students[globalDict[usr_id]], callback.data),
                                         reply_markup=stud_application_ikb,
                                         parse_mode='HTML')


@dp.callback_query_handler(text='approve')
async def approve_student(callback: types.CallbackQuery):
    """
    Функция одобрения заявки студента.
    """
    usr_id = str(callback.from_user.id)
    student_id = current_student(globalDict[usr_id])
    add_application(student_id, callback.from_user.id, 1)
    globalDict[usr_id] -= 1
    write_user_values("globalDict", globalDict)

    text = ('Ваша заявка была <b>одобрена</b>.'
            'Вы можете выбрать задачу из списка доступных задач.\n'
            'Чат для связи доступен по <a href="https://t.me/+FShhqiWUDJRjODky">этой ссылке</a>')

    await bot.send_message(student_id, text, reply_markup=student_task_show,
                           parse_mode='HTML', disable_web_page_preview=True)
    await callback.message.edit_text('Заявка одобрена.', reply_markup=stud_application_ikb_2)


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
    student_id = current_student(globalDict[usr_id])
    add_application(student_id, callback.from_user.id, 0)
    count_students, students = count_get_students()

    if count_students and (globalDict[usr_id] >= count_students or globalDict[usr_id] < count_students):
        globalDict[usr_id] = 0
        write_user_values("globalDict", globalDict)

    await state.finish()
    try:
        await bot.send_message(student_id, 'Ваша заявка была <b>отклонена</b>.', parse_mode='HTML')
        await callback.message.edit_text('Заявка отклонена.', reply_markup=stud_application_ikb_2)
    except Exception as e:
        logging.exception(e)
        await callback.message.edit_text('ID студента не был найден.', reply_markup=stud_application_ikb_2)
