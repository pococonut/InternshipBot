from commands.show import print_stud
from db.commands import select_chosen_tasks, select_user
from keyboard import admin_ikb, task_worker_stud, back_to_std
from aiogram import types, Dispatcher


# ----------------- Просмотр выбранной студентом задачи (для сотрудника) -----------------

page_tws = 0


async def worker_chosen_t(callback: types.CallbackQuery):
    global page_tws
    # page_tws = 0
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        try:
            count_tasks = len(tasks)
            student = select_user(tasks[page_tws].student_id)
            await callback.message.edit_text(f"<b>№</b> {page_tws + 1}/{count_tasks}\n\n"
                                             f"👨‍🎓<b>Студент</b>\n\n"
                                             f"<b>ФИО:</b> {student.student_name}\n\n"
                                             f"<b>Направление:</b> {student.specialties}\n\n"
                                             f"<b>Курс:</b> {student.course}\n\n"
                                             f"<b>Знания:</b> {student.knowledge}\n\n"
                                             f"———————————————————\n\n"
                                             f"📚<b>Выбранная задача</b>\n\n"
                                             f"<b>Название:</b> {tasks[page_tws].task_name}\n\n"
                                             f"<b>Описание:</b> {tasks[page_tws].task_description}\n\n",
                                             parse_mode='HTML',
                                             reply_markup=task_worker_stud,
                                             disable_web_page_preview=True)
        except Exception as e:
            print(e)


async def task_ws_show(callback: types.CallbackQuery):
    global page_tws
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        count_tasks = len(tasks)
        s = ''
        if callback.data == 'tws_right':
            page_tws += 1
            if page_tws == count_tasks:
                page_tws = 0
            p_tws = page_tws
            if page_tws <= -1:
                p_tws = count_tasks + page_tws
            s = f"<b>№</b> {p_tws + 1}/{count_tasks}\n\n"

        if callback.data == 'tws_left':
            page_tws -= 1
            p_tws = 0
            if page_tws == (-1) * count_tasks:
                page_tws = 0
            print(page_tws)
            if page_tws <= -1:
                p_tws = count_tasks

            s = f"<b>№</b> {(p_tws + page_tws) + 1}/{count_tasks}\n\n"

        student = select_user(tasks[page_tws].student_id)
        await callback.message.edit_text(s + f"👨‍🎓<b>Студент</b>\n\n"
                                             f"<b>ФИО:</b> {student.student_name}\n\n"
                                             f"<b>Направление:</b> {student.specialties}\n\n"
                                             f"<b>Курс:</b> {student.course}\n\n"
                                             f"<b>Знания:</b> {student.knowledge}\n\n"
                                             f"——————————————————\n\n"
                                             f"📚<b>Выбранная задача</b>\n\n"
                                             f"<b>Название:</b> {tasks[page_tws].task_name}\n\n"
                                             f"<b>Описание:</b> {tasks[page_tws].task_description}\n\n",
                                         parse_mode='HTML',
                                         reply_markup=task_worker_stud,
                                         disable_web_page_preview=True)


async def show_more_stud(callback: types.CallbackQuery):
    tasks = select_chosen_tasks(callback.from_user.id)
    student = select_user(tasks[page_tws].student_id)

    await callback.message.edit_text(f"👨‍🎓<b>Студент</b>\n\n" + print_stud(student), parse_mode='HTML',
                                     reply_markup=back_to_std)


def register_handlers_task_selected_worker(dp: Dispatcher):
    dp.register_callback_query_handler(worker_chosen_t, text='worker_chosen_tasks')
    dp.register_callback_query_handler(task_ws_show, text=['tws_right', 'tws_left'])
    dp.register_callback_query_handler(show_more_stud, text='tws_student')
