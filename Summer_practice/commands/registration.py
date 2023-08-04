from commands.back import back_func
from db.commands import user_type, stud_approve, select_user, register_student
from keyboard import back_cont_ikb, admin_ikb, worker_ikb, stud_is_approve, ikb_3, back_ikb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import string
import re


FORM = """
Для подачи заявки необходиммо ввести следующие данные:

<em>ФИО
ВУЗ
Факультет
Направление
Кафедра
Курс
Группа
Темы курсовых работ
Ваши знания</em>

<b>отдельными сообщениями</b>.
"""

# ---------------- Регистрация\подача заявки для студента ----------------


class Student(StatesGroup):
    student_name = State()
    university = State()
    faculty = State()
    specialties = State()
    department = State()
    course = State()
    group = State()
    coursework = State()
    knowledge = State()


async def registration_command(message: types.Message):
    user_exist = user_type(message.from_user.id)
    if not user_exist:
        await message.answer(FORM, parse_mode='HTML',
                             reply_markup=back_cont_ikb)
    else:
        usr = {'student': 'студент',
               'admin': 'администратор',
               'director': 'директор',
               'worker': 'сотрудник'}

        if user_exist[0] in ('admin', 'director'):
            keyboard = admin_ikb
        elif user_exist[0] == 'worker':
            keyboard = worker_ikb
        elif user_exist[0] == 'student':
            approve = stud_approve(message.from_user.id)
            if approve is not None and approve[0]:
                keyboard = stud_is_approve
                print(user_exist[0])
                print(approve)
            else:
                keyboard = ikb_3
        print(user_exist[0])
        await message.answer(f'Вы зарегестрированы как <b>{usr.get(user_exist[0])}</b>.', parse_mode='HTML',
                             reply_markup=keyboard)


async def cont_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>",
                                     parse_mode='HTML', reply_markup=back_ikb)
    await Student.student_name.set()


async def get_student_name(message: types.Message, state: FSMContext):
    student_exist = select_user(message.from_user.id)
    if student_exist:
        await state.finish()
        await state.reset_state(with_data=False)
    else:
        if len(message.text.split()) != 3 or any(chr.isdigit() for chr in message.text) or any(
                chr in string.punctuation for chr in message.text):
            await message.answer('ФИО введено в некорректном формате', parse_mode='HTML')
            return
        await state.update_data(student_name=" ".join([i.capitalize() for i in message.text.split()]))
        await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
        await Student.next()


async def get_university(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text.upper())
    await message.answer("Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>",
                         parse_mode='HTML')
    await Student.next()


async def get_faculty(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text.capitalize())
    await message.answer("Введите <b>Направление</b> в формате: <em>Фундаментальные математика и механика</em>",
                         parse_mode='HTML')
    await Student.next()


async def get_specialties(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text.capitalize())
    await message.answer("Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>",
                         parse_mode='HTML')
    await Student.next()


async def get_department(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text.upper())
    await message.answer("Введите <b>Курс</b> в формате: <em>2</em>", parse_mode='HTML')
    await Student.next()


async def get_course(message: types.Message, state=FSMContext):
    if len(message.text) != 1 or any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('Курс введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(course=message.text)
    await message.answer("Введите <b>Группу</b> в формате: <em>23/3</em>", parse_mode='HTML')
    await Student.next()


async def get_group(message: types.Message, state=FSMContext):
    if (re.fullmatch('\d{,3}\D\d', message.text) is None) or any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation.replace('/', '') for chr in message.text) or ' ' in message.text:
        await message.answer('Группа введена в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(group=message.text)
    await message.answer(
        'Введите <b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате:'
        ' <em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>',
        parse_mode='HTML')
    await Student.next()


async def get_coursework(message: types.Message, state=FSMContext):
    await state.update_data(coursework=message.text)
    await message.answer(
        "Введите <b>Ваши знания</b> (при отсутствии введите: 'Нет') в формате: <em>Python, SQL, C++, JS</em>",
        parse_mode='HTML')
    await Student.next()


async def get_knowledge(message: types.Message, state=FSMContext):
    await state.update_data(knowledge=message.text)
    data = await state.get_data()
    await message.answer(f"🧑‍💻<b>Ваши данные</b>\n\n"
                         f"<b>ФИО:</b> {data['student_name']}\n\n"
                         f"<b>ВУЗ:</b> {data['university']}\n\n"
                         f"<b>Факультет:</b> {data['faculty']}\n\n"
                         f"<b>Специальность:</b> {data['specialties']}\n\n"
                         f"<b>Кафедра:</b> {data['department']}\n\n"
                         f"<b>Курс:</b> {data['course']}\n\n"
                         f"<b>Группа:</b> {data['group']}\n\n"
                         f"<b>Курсовые:</b> {data['coursework']}\n\n"
                         f"<b>Знания:</b> {data['knowledge']}\n\n", parse_mode='HTML')
    student = register_student(message.from_user.id, data)
    if student:
        await message.answer(f'Регистрация окончена.\n\n'
                             f'После рассмотрения заявки сотрудниками, вам придет уведомление.', parse_mode='HTML',
                             reply_markup=ikb_3)
    await state.finish()



def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(registration_command, commands=['student'])
    dp.register_callback_query_handler(cont_command, text='continue', state="*")
    dp.register_message_handler(get_student_name, state=Student.student_name)
    dp.register_message_handler(get_university, state=Student.university)
    dp.register_message_handler(get_faculty, state=Student.faculty)
    dp.register_message_handler(get_specialties, state=Student.specialties)
    dp.register_message_handler(get_department, state=Student.department)
    dp.register_message_handler(get_course, state=Student.course)
    dp.register_message_handler(get_group, state=Student.group)
    dp.register_message_handler(get_coursework, state=Student.coursework)
    dp.register_message_handler(get_knowledge, state=Student.knowledge)
    dp.register_callback_query_handler(back_func, text='back', state="*")
