from db.commands import stud_approve, select_added_users, select_task, select_user, select_all_users
from keyboard import exp_ikb
from aiogram import types, Dispatcher
import openpyxl


# ------------------- Экспорт данных -------------------

async def export(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите команду.", parse_mode='HTML', reply_markup=exp_ikb)


async def export_task(callback: types.CallbackQuery):
    tasks = select_task()
    wb = openpyxl.Workbook()

    sheet = wb.active
    sheet.title = "Задачи"

    c2 = sheet.cell(row=1, column=1)
    c2.value = "Сотрудник"
    c3 = sheet.cell(row=1, column=2)
    c3.value = "Студент"
    c4 = sheet.cell(row=1, column=3)
    c4.value = "Название"
    c5 = sheet.cell(row=1, column=4)
    c5.value = "Цель"
    c6 = sheet.cell(row=1, column=5)
    c6.value = "Описание"
    c7 = sheet.cell(row=1, column=6)
    c7.value = "Задачи"
    c8 = sheet.cell(row=1, column=7)
    c8.value = "Требования к технологиям"
    c9 = sheet.cell(row=1, column=8)
    c9.value = "Новые навыки"
    c10 = sheet.cell(row=1, column=9)
    c10.value = "Количество людей"
    c11 = sheet.cell(row=1, column=10)
    c11.value = "Материалы"

    for i in range(2, len(tasks) + 2):
        index = i - 2

        s2 = sheet.cell(row=i, column=1)
        s2.value = select_user(tasks[index].from_id).name

        s3 = sheet.cell(row=i, column=2)
        s3.value = select_user(tasks[index].student_id).name if tasks[index].student_id is not None else None

        s4 = sheet.cell(row=i, column=3)
        s4.value = tasks[index].task_name

        s5 = sheet.cell(row=i, column=4)
        s5.value = tasks[index].task_goal

        s6 = sheet.cell(row=i, column=5)
        s6.value = tasks[index].task_description

        s7 = sheet.cell(row=i, column=6)
        s7.value = tasks[index].task_tasks

        s8 = sheet.cell(row=i, column=7)
        s8.value = tasks[index].task_technologies

        s9 = sheet.cell(row=i, column=8)
        s9.value = tasks[index].task_new_skills

        s10 = sheet.cell(row=i, column=9)
        s10.value = tasks[index].num_people

        s11 = sheet.cell(row=i, column=10)
        s11.value = tasks[index].materials

    wb.save(r"files\Задачи.xlsx")
    doc = open(r"files\Задачи.xlsx", 'rb')

    await callback.answer()
    await callback.message.answer_document(doc)


async def export_worker(callback: types.CallbackQuery):

    wb = openpyxl.Workbook()

    sheet = wb.active
    sheet.title = "Сотрудники"

    c1 = sheet.cell(row=1, column=1)
    c1.value = "Тип"
    c2 = sheet.cell(row=1, column=2)
    c2.value = "Имя"
    c3 = sheet.cell(row=1, column=3)
    c3.value = "Номер Телефона"
    c4 = sheet.cell(row=1, column=4)
    c4.value = "Дата регистрации"
    c5 = sheet.cell(row=1, column=5)
    c5.value = "Дата изменения"
    c6 = sheet.cell(row=1, column=6)
    c6.value = "Логин"
    c7 = sheet.cell(row=1, column=7)
    c7.value = "Пароль"

    workers = select_all_users()

    i = 2
    for w in range(2, len(workers) + 2):
        index = w - 2

        if workers[index].type != 'student':

            s1 = sheet.cell(row=i, column=1)
            s1.value = workers[index].type

            s2 = sheet.cell(row=i, column=2)
            s2.value = workers[index].name

            s3 = sheet.cell(row=i, column=3)
            s3.value = workers[index].phone

            s4 = sheet.cell(row=i, column=4)
            s4.value = workers[index].reg_date

            s5 = sheet.cell(row=i, column=5)
            s5.value = workers[index].upd_date

            s6 = sheet.cell(row=i, column=6)
            s6.value = workers[index].login

            s7 = sheet.cell(row=i, column=7)
            s7.value = workers[index].password

            i += 1

    wb.save(r"files\Сотрудники.xlsx")
    doc = open(r"files\Сотрудники.xlsx", 'rb')

    await callback.answer()
    await callback.message.answer_document(doc)


async def export_applications(callback: types.CallbackQuery):

    wb = openpyxl.Workbook()

    sheet = wb.active
    sheet.title = "Заявки"

    c1 = sheet.cell(row=1, column=1)
    c1.value = "ФИО"
    c2 = sheet.cell(row=1, column=2)
    c2.value = "Номер Телефона"
    c3 = sheet.cell(row=1, column=3)
    c3.value = "ВУЗ"
    c4 = sheet.cell(row=1, column=4)
    c4.value = "Факультет"
    c5 = sheet.cell(row=1, column=5)
    c5.value = "Направление"
    c6 = sheet.cell(row=1, column=6)
    c6.value = "Кафедра"
    c7 = sheet.cell(row=1, column=7)
    c7.value = "Курс"
    c8 = sheet.cell(row=1, column=8)
    c8.value = "Группа"
    c9 = sheet.cell(row=1, column=9)
    c9.value = "Курсовые"
    c10 = sheet.cell(row=1, column=10)
    c10.value = "Знания"

    students = select_all_users()

    i = 2
    for a in range(2, len(students) + 2):
        index = a - 2

        if students[index].type == 'student':

            s1 = sheet.cell(row=i, column=1)
            s1.value = students[index].student_name

            s2 = sheet.cell(row=i, column=2)
            s2.value = students[index].phone

            s3 = sheet.cell(row=i, column=3)
            s3.value = students[index].university

            s4 = sheet.cell(row=i, column=4)
            s4.value = students[index].faculty

            s5 = sheet.cell(row=i, column=5)
            s5.value = students[index].specialties

            s6 = sheet.cell(row=i, column=6)
            s6.value = students[index].department

            s7 = sheet.cell(row=i, column=7)
            s7.value = students[index].course

            s8 = sheet.cell(row=i, column=8)
            s8.value = students[index].group

            s9 = sheet.cell(row=i, column=9)
            s9.value = students[index].coursework

            s10 = sheet.cell(row=i, column=10)
            s10.value = students[index].knowledge

            i += 1

    wb.save(r"files\Заявки.xlsx")
    doc = open(r"files\Заявки.xlsx", 'rb')

    await callback.answer()
    await callback.message.answer_document(doc)


async def export_approved(callback: types.CallbackQuery):

    wb = openpyxl.Workbook()

    sheet = wb.active
    sheet.title = "Заявки"

    c1 = sheet.cell(row=1, column=1)
    c1.value = "ФИО"
    c2 = sheet.cell(row=1, column=2)
    c2.value = "Номер Телефона"
    c3 = sheet.cell(row=1, column=3)
    c3.value = "ВУЗ"
    c4 = sheet.cell(row=1, column=4)
    c4.value = "Факультет"
    c5 = sheet.cell(row=1, column=5)
    c5.value = "Направление"
    c6 = sheet.cell(row=1, column=6)
    c6.value = "Кафедра"
    c7 = sheet.cell(row=1, column=7)
    c7.value = "Курс"
    c8 = sheet.cell(row=1, column=8)
    c8.value = "Группа"
    c9 = sheet.cell(row=1, column=9)
    c9.value = "Курсовые"
    c10 = sheet.cell(row=1, column=10)
    c10.value = "Знания"

    students = select_all_users()

    i = 2
    for s in range(2, len(students) + 2):
        index = s - 2

        if stud_approve(students[index].telegram_id):

            s1 = sheet.cell(row=i, column=1)
            s1.value = students[index].student_name

            s2 = sheet.cell(row=i, column=2)
            s2.value = students[index].phone

            s3 = sheet.cell(row=i, column=3)
            s3.value = students[index].university

            s4 = sheet.cell(row=i, column=4)
            s4.value = students[index].faculty

            s5 = sheet.cell(row=i, column=5)
            s5.value = students[index].specialties

            s6 = sheet.cell(row=i, column=6)
            s6.value = students[index].department

            s7 = sheet.cell(row=i, column=7)
            s7.value = students[index].course

            s8 = sheet.cell(row=i, column=8)
            s8.value = students[index].group

            s9 = sheet.cell(row=i, column=9)
            s9.value = students[index].coursework

            s10 = sheet.cell(row=i, column=10)
            s10.value = students[index].knowledge

            i += 1

    wb.save(r"files\Принятые студенты.xlsx")
    doc = open(r"files\Принятые студенты.xlsx", 'rb')

    await callback.answer()
    await callback.message.answer_document(doc)


async def export_added(callback: types.CallbackQuery):

    wb = openpyxl.Workbook()

    sheet = wb.active
    sheet.title = "Добавленные аккаунты"

    c1 = sheet.cell(row=1, column=1)
    c1.value = "Логин"
    c2 = sheet.cell(row=1, column=2)
    c2.value = "Пароль"
    c3 = sheet.cell(row=1, column=3)
    c3.value = "Тип"

    added_users = select_added_users()
    print(len(added_users))
    for i in range(2, len(added_users) + 2):
        index = i - 2
        print(added_users[index].type)
        s1 = sheet.cell(row=i, column=1)
        s1.value = added_users[index].login

        s2 = sheet.cell(row=i, column=2)
        s2.value = added_users[index].password

        s3 = sheet.cell(row=i, column=3)
        s3.value = added_users[index].type

    wb.save(r"files\Добавленные аккаунты.xlsx")
    doc = open(r"files\Добавленные аккаунты.xlsx", 'rb')

    await callback.answer()
    await callback.message.answer_document(doc)


def register_handlers_export(dp: Dispatcher):
    dp.register_callback_query_handler(export, text='export')
    dp.register_callback_query_handler(export_task, text='exp_task')
    dp.register_callback_query_handler(export_worker, text='exp_worker')
    dp.register_callback_query_handler(export_applications, text='exp_appl')
    dp.register_callback_query_handler(export_approved, text='exp_approved')
    dp.register_callback_query_handler(export_added, text='exp_added')