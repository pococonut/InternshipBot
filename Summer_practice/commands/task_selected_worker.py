from commands.show import print_stud
from db.commands import select_chosen_tasks, select_user
from keyboard import admin_ikb, task_worker_stud, back_to_std
from aiogram import types, Dispatcher


# ----------------- Просмотр выбранной студентом задачи (для сотрудника) -----------------


globalDict_pagesTws = dict()


async def worker_chosen_t(callback: types.CallbackQuery):
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_pagesTws:
            globalDict_pagesTws[usr_id] = 0
        print(globalDict_pagesTws)

        count_tasks = len(tasks)
        student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
        if not student:
            await callback.message.edit_text('Заявки студентов не были рассмотрены.', reply_markup=admin_ikb)
        else:
            await callback.message.edit_text(f"<b>№</b> {globalDict_pagesTws[usr_id] + 1}/{count_tasks}\n\n"
                                             f"👨‍🎓<b>Студент</b>\n\n"
                                             f"<b>ФИО:</b> {student.student_name}\n\n"
                                             f"<b>Направление:</b> {student.specialties}\n\n"
                                             f"<b>Курс:</b> {student.course}\n\n"
                                             f"<b>Знания:</b> {student.knowledge}\n\n"
                                             f"———————————————————\n\n"
                                             f"📚<b>Выбранная задача</b>\n\n"
                                             f"<b>Название:</b> {tasks[globalDict_pagesTws[usr_id]].task_name}\n\n"
                                             f"<b>Описание:</b> {tasks[globalDict_pagesTws[usr_id]].task_description}\n\n",
                                             parse_mode='HTML',
                                             reply_markup=task_worker_stud,
                                             disable_web_page_preview=True)


async def task_ws_show(callback: types.CallbackQuery):
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_pagesTws:
            globalDict_pagesTws[usr_id] = 0

        count_tasks = len(tasks)
        s = ''
        if callback.data == 'tws_right':
            globalDict_pagesTws[usr_id] += 1
            if globalDict_pagesTws[usr_id] == count_tasks:
                globalDict_pagesTws[usr_id] = 0
            p_tws = globalDict_pagesTws[usr_id]
            if globalDict_pagesTws[usr_id] <= -1:
                p_tws = count_tasks + globalDict_pagesTws[usr_id]
            s = f"<b>№</b> {p_tws + 1}/{count_tasks}\n\n"

        if callback.data == 'tws_left':
            globalDict_pagesTws[usr_id] -= 1
            p_tws = 0
            if globalDict_pagesTws[usr_id] == (-1) * count_tasks:
                globalDict_pagesTws[usr_id] = 0
            print(globalDict_pagesTws[usr_id])
            if globalDict_pagesTws[usr_id] <= -1:
                p_tws = count_tasks

            s = f"<b>№</b> {(p_tws + globalDict_pagesTws[usr_id]) + 1}/{count_tasks}\n\n"

        student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
        print(globalDict_pagesTws)
        await callback.message.edit_text(s + f"👨‍🎓<b>Студент</b>\n\n"
                                             f"<b>ФИО:</b> {student.student_name}\n\n"
                                             f"<b>Направление:</b> {student.specialties}\n\n"
                                             f"<b>Курс:</b> {student.course}\n\n"
                                             f"<b>Знания:</b> {student.knowledge}\n\n"
                                             f"——————————————————\n\n"
                                             f"📚<b>Выбранная задача</b>\n\n"
                                             f"<b>Название:</b> {tasks[globalDict_pagesTws[usr_id]].task_name}\n\n"
                                             f"<b>Описание:</b> {tasks[globalDict_pagesTws[usr_id]].task_description}\n\n",
                                         parse_mode='HTML',
                                         reply_markup=task_worker_stud,
                                         disable_web_page_preview=True)


async def show_more_stud(callback: types.CallbackQuery):
    tasks = select_chosen_tasks(callback.from_user.id)
    usr_id = str(callback.from_user.id)
    student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
    await callback.message.edit_text(f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student), parse_mode='HTML',
                                     reply_markup=back_to_std)


def register_handlers_task_selected_worker(dp: Dispatcher):
    dp.register_callback_query_handler(worker_chosen_t, text='worker_chosen_tasks')
    dp.register_callback_query_handler(task_ws_show, text=['tws_right', 'tws_left'])
    dp.register_callback_query_handler(show_more_stud, text='tws_student')
