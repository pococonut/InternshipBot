"""@dp.callback_query_handler(text='approve')
async def approve_stud(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]

    student_id = students[page_stud].telegram_id
    print(page_stud, student_id, students[page_stud].student_name)
    add_application(student_id, callback.from_user.id, 1)

    await callback.message.answer('Заявка одобрена.', reply_markup=stud_appl_ikb_2)


def approve_reject(page_s, from_id, b):
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    student_id = students[page_s].telegram_id
    print(page_stud, student_id, students[page_s].student_name)
    add_application(student_id, from_id, b)"""
