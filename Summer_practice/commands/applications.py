from commands.back import back_func
from commands.task_actions import show_task
from db.commands import select_students, select_applications, add_application
from keyboard import admin_ikb, stud_appl_ikb, student_task_show, stud_appl_back_ikb, del_stud_ikb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import bot


# --------------------- Просмотр заявок студентов ---------------------


globalDict = dict()


def print_stud(s):
    stud = f"<b>ФИО:</b> {s.student_name}\n\n" \
           f"<b>ВУЗ:</b> {s.university}\n\n" \
           f"<b>Факультет:</b> {s.faculty}\n\n" \
           f"<b>Специальность:</b> {s.specialties}\n\n" \
           f"<b>Кафедра:</b> {s.department}\n\n" \
           f"<b>Курс:</b> {s.course}\n\n" \
           f"<b>Группа:</b> {s.group}\n\n" \
           f"<b>Курсовые:</b> {s.coursework}\n\n" \
           f"<b>Знания:</b> {s.knowledge}\n\n" \
           f"<b>Дата регистрации:</b> {s.reg_date}\n"
    return stud


async def show_stud(callback: types.CallbackQuery):
    usr_id = str(callback.from_user.id)
    if usr_id not in globalDict:
        globalDict[usr_id] = 0
    print(globalDict)
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]

    if not students:
        try:
            await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.',
                                             reply_markup=admin_ikb)
        except Exception as e:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент заявок нет.\nЗагляните позже.',
                                          reply_markup=admin_ikb)
    else:
        count_students = len(all_students) - len(applications)
        await callback.message.edit_text(f"<b>№</b> {globalDict[usr_id] + 1}/{count_students}\n\n" + print_stud(students[globalDict[usr_id]]),
                                         reply_markup=stud_appl_ikb, parse_mode='HTML')


async def std_rl(callback: types.CallbackQuery):
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict:
            globalDict[usr_id] = 0

        count_students = len(all_students) - len(applications)
        s = ''
        if callback.data == 'right_stud':
            globalDict[usr_id] += 1
            if globalDict[usr_id] == count_students:
                globalDict[usr_id] = 0
            p_rs = globalDict[usr_id]
            if globalDict[usr_id] <= -1:
                p_rs = count_students + globalDict[usr_id]
            s = f"<b>№</b> {p_rs + 1}/{count_students}\n\n"

        if callback.data == 'left_stud':
            globalDict[usr_id] -= 1
            p_ls = 0
            if globalDict[usr_id] == (-1) * count_students:
                globalDict[usr_id] = 0
            if globalDict[usr_id] <= -1:
                p_ls = count_students
            s = f"<b>№</b> {(p_ls + globalDict[usr_id]) + 1}/{count_students}\n\n"

        print(globalDict)
        await callback.message.edit_text(s + print_stud(students[globalDict[usr_id]]), reply_markup=stud_appl_ikb, parse_mode='HTML')


# ---------------------- Принятие\отклонение заявки студента ----------------------


def current_student(page_s):
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    student_id = students[page_s].telegram_id
    print(page_s, student_id, students[page_s].student_name)
    return student_id


async def approve_stud(callback: types.CallbackQuery):
    usr_id = str(callback.from_user.id)
    student_id = current_student(globalDict[usr_id])
    add_application(student_id, callback.from_user.id, 1)
    try:
        await bot.send_message(student_id, 'Ваша заявка была <b>одобрена</b>.\n\nВы можете выбрать задачу из списка '
                               'доступных задач.\n\nЧат для взаимодействия с сотрудниками доступен по ссылке - https://t.me/+FShhqiWUDJRjODky',
                               reply_markup=student_task_show, parse_mode='HTML', disable_web_page_preview=True)
        await callback.message.edit_text('Заявка одобрена.', reply_markup=stud_appl_back_ikb)
    except Exception as e:
        await callback.message.edit_text('ID студента не был найден.', reply_markup=stud_appl_back_ikb)


class StudDel(StatesGroup):
    del_s = State()


async def reject_stud(callback: types.CallbackQuery):
    await callback.message.edit_text('Отклонить заявку?', parse_mode='HTML', reply_markup=del_stud_ikb)
    await StudDel.del_s.set()


async def reject_stud_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(del_s=callback.data)
    usr_id = str(callback.from_user.id)
    student_id = current_student(globalDict[usr_id])
    add_application(student_id, callback.from_user.id, 0)
    await state.finish()
    try:
        await bot.send_message(student_id, 'Ваша заявка была <b>отклонена</b>.', parse_mode='HTML')
        await callback.message.edit_text('Заявка отклонена.', reply_markup=stud_appl_back_ikb)
    except Exception as e:
        await callback.message.edit_text('ID студента не был найден.', reply_markup=stud_appl_back_ikb)


def register_handlers_applications(dp: Dispatcher):
    dp.register_callback_query_handler(show_task, text='show_task')
    dp.register_callback_query_handler(show_stud, text='show_students')
    dp.register_callback_query_handler(std_rl, text=['right_stud', 'left_stud'])
    dp.register_callback_query_handler(approve_stud, text='approve')
    dp.register_callback_query_handler(reject_stud, text='reject')
    dp.register_callback_query_handler(reject_stud_yes, text='reject_yes', state=StudDel.del_s)
    dp.register_callback_query_handler(back_func, text='back', state="*")