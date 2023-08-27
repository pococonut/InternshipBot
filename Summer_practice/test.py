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

        s, globalDict_pagesTws[usr_id] = navigation(callback.data, globalDict_pagesTws[usr_id], count_tasks)

        if callback.data == 'worker_chosen_tasks':

            if len(tasks[globalDict_pagesTws[usr_id]].student_id.split()) == 1:

                student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
                if globalDict_pagesTws[usr_id] <= -1:
                    num = count_tasks
                else:
                    num = globalDict_pagesTws[usr_id] + 1
                s_sh = show_stud_task(student, tasks[globalDict_pagesTws[usr_id]])

            else:
                lst = tasks[globalDict_pagesTws[usr_id]].student_id.split()
                for stud in lst:
                    student_lst.append(select_user(stud))
                s_sh = ''
                for stud in student_lst:
                    s_sh += show_short_stud(stud)
                s_sh += f"📚<b>Выбранная задача</b>\n\n" + short_long_task(tasks[globalDict_pagesTws[usr_id]])
                num = globalDict_pagesTws[usr_id] + 1

            await callback.message.edit_text(f"<b>№</b> {num}/{count_tasks}\n\n" + s_sh,
                                             parse_mode='HTML',
                                             reply_markup=task_worker_stud,
                                             disable_web_page_preview=True)
        else:
            if len(tasks[globalDict_pagesTws[usr_id]].student_id.split()) == 1:

                student = select_user(tasks[globalDict_pagesTws[usr_id]].student_id)
                await callback.message.edit_text(s + show_stud_task(student, tasks[globalDict_pagesTws[usr_id]]),
                                                 parse_mode='HTML',
                                                 reply_markup=task_worker_stud,
                                                 disable_web_page_preview=True)
            else:
                s_sh = ''
                for stud in student_lst:
                    s_sh += show_short_stud(stud)
                s_sh += f"📚<b>Выбранная задача</b>\n\n" + short_long_task(tasks[globalDict_pagesTws[usr_id]])
                await callback.message.edit_text(f"<b>№</b> {globalDict_pagesTws[usr_id] + 1}/{count_tasks}\n\n" +
                                                 s_sh,
                                                 parse_mode='HTML',
                                                 reply_markup=task_worker_stud,
                                                 disable_web_page_preview=True)