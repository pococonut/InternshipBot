from commands.task_actions import short_long_task
from create import dp
from aiogram import types
from keyboard import task_worker_stud, back_to_std
from commands.general import print_stud, get_keyboard, navigation
from db.commands import select_chosen_tasks, select_user


globalDict_pagesTws = dict()


def show_stud_task(s, t):
    """
    Функция вывода краткой информации о Задаче и Студенте, выбравшем ее.
    :param s: Строка модели БД, относящаяся к конкретному студенту, с информацией о нем.
    :param t: Строка модели БД, относящаяся к конкретной задаче, с информацией о ней.
    :return:
    """
    v = f"👨‍🎓<b>Студент\ка</b>\n\n" \
        f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n\n" \
        f"<b>Направление:</b> {s.specialties}\n\n" \
        f"<b>Курс:</b> {s.course}\n\n" \
        f"<b>Знания:</b> {s.knowledge}\n\n" \
        f"———————————————————\n\n" \
        f"📚<b>Выбранная задача</b>\n\n" \
        f"<b>Название:</b> {t.task_name}\n\n" \
        f"<b>Описание:</b> {t.task_description}\n\n"
    return v


def show_short_stud(s):
    """
    Функция вывода краткой информации о Задаче и Студенте, выбравшем ее.
    :param s: Строка модели БД, относящаяся к конкретному студенту, с информацией о нем.
    :param t: Строка модели БД, относящаяся к конкретной задаче, с информацией о ней.
    :return:
    """
    v = f"👨‍🎓<b>Студент\ка</b>\n\n" \
        f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n\n" \
        f"<b>Направление:</b> {s.specialties}\n\n" \
        f"<b>Курс:</b> {s.course}\n\n" \
        f"<b>Знания:</b> {s.knowledge}\n\n" \
        f"———————————————————\n\n"
    return v


@dp.callback_query_handler(text=['worker_chosen_tasks', 'tws_right', 'tws_left'])
async def worker_chosen_t(callback: types.CallbackQuery):
    """
    Функция просмотра выбранных студентами задач для сотрудника.
    """
    tasks = select_chosen_tasks(callback.from_user.id)
    keyboard = get_keyboard(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=keyboard)
        await callback.answer()
    else:
        usr_id = str(callback.from_user.id)
        count_tasks = len(tasks)
        student_lst = []

        if usr_id not in globalDict_pagesTws:
            globalDict_pagesTws[usr_id] = 0

        if len(tasks[globalDict_pagesTws[usr_id]].student_id.split()) == 1:
            student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
        else:
            lst = tasks[globalDict_pagesTws[usr_id]].student_id.split()
            for s in lst:
                student_lst.append(select_user(s))

        if callback.data == 'worker_chosen_tasks':

            if student_lst:
                s_sh = ''
                for s in student_lst:
                    s_sh += show_short_stud(s)
                s_sh += f"📚<b>Выбранная задача</b>\n\n" + short_long_task(tasks[globalDict_pagesTws[usr_id]])
                await callback.message.edit_text(f"<b>№</b> {globalDict_pagesTws[usr_id] + 1}/{count_tasks}\n\n" +
                                                 s_sh,
                                                 parse_mode='HTML',
                                                 reply_markup=task_worker_stud,
                                                 disable_web_page_preview=True)
            else:
                await callback.message.edit_text(f"<b>№</b> {globalDict_pagesTws[usr_id] + 1}/{count_tasks}\n\n" +
                                                 show_stud_task(student, tasks[globalDict_pagesTws[usr_id]]),
                                                 parse_mode='HTML',
                                                 reply_markup=task_worker_stud,
                                                 disable_web_page_preview=True)
        else:

            print(globalDict_pagesTws[usr_id])

            s, globalDict_pagesTws[usr_id] = navigation(callback.data, globalDict_pagesTws[usr_id], count_tasks)
            #student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
            print(globalDict_pagesTws[usr_id])
            await callback.message.edit_text(s + show_stud_task(student, tasks[globalDict_pagesTws[usr_id]]),
                                             parse_mode='HTML',
                                             reply_markup=task_worker_stud,
                                             disable_web_page_preview=True)


@dp.callback_query_handler(text='tws_student')
async def show_more_stud(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации о студенте.
    """
    usr_id = str(callback.from_user.id)
    tasks = select_chosen_tasks(usr_id)
    count_students = tasks[globalDict_pagesTws[usr_id]].student_id

    if len(count_students.split()) == 1:
        student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
        await callback.message.edit_text(f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student), parse_mode='HTML',
                                     reply_markup=back_to_std)
    else:
        students_sh = ''
        students_lst = count_students.split()
        for s_id in count_students.split():
            student = select_user(s_id)
            students_sh += f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student)
            if students_lst[-1] != s_id:
                students_sh += "———————————————————\n\n"

        await callback.message.edit_text(students_sh, parse_mode='HTML',
                                         reply_markup=back_to_std)