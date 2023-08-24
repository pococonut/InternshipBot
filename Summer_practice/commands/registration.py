import re
import string
import phonenumbers
from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboard import back_cont_ikb, ikb_3, back_ikb
from db.commands import select_user, registration_user
from aiogram.dispatcher.filters.state import StatesGroup, State


FORM = """
Для подачи заявки необходимо ввести следующие данные:

<em>ФИО
Номер телефона
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


class Student(StatesGroup):
    student_name = State()
    phone = State()
    university = State()
    faculty = State()
    specialties = State()
    department = State()
    course = State()
    group = State()
    coursework = State()
    knowledge = State()


@dp.callback_query_handler(text='student')
async def registration_command(callback: types.CallbackQuery):
    """
    Функция вывода сообщения для ознакомления с необходимыми для подачи заявки параметрами.
    """
    await callback.message.edit_text(FORM, parse_mode='HTML', reply_markup=back_cont_ikb)


@dp.callback_query_handler(text='continue', state="*")
async def cont_command(callback: types.CallbackQuery):
    """
    Функция начала ввода параметров заявки.
    """
    await callback.message.edit_text("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>",
                                     parse_mode='HTML', reply_markup=back_ikb)
    await Student.student_name.set()


@dp.message_handler(state=Student.student_name)
async def get_student_name(message: types.Message, state: FSMContext):
    """
    Функция получения и проверки параметра заявки - ФИО.
    """
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
        await message.answer("Введите <b>Номер телефона, привязанный к telegram</b> в формате: <code><em>+79999999999</em></code>", parse_mode='HTML')
        await Student.next()


@dp.message_handler(state=Student.phone)
async def get_phone(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Номер телефона.
    """
    try:
        phonenumbers.parse(message.text)
        await state.update_data(phone=message.text.upper())
        await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
        await Student.next()
    except:
        await message.answer('Номер телефона введен в некорректном формате', parse_mode='HTML')
        return


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Университет.
    """
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text.upper())
    await message.answer("Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Факультет.
    """
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text.capitalize())
    await message.answer("Введите <b>Направление</b> в формате: <em>Фундаментальные математика и механика</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Специальность.
    """
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text.capitalize())
    await message.answer("Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Кафедра.
    """
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text.upper())
    await message.answer("Введите <b>Курс</b> в формате: <em>2</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.course)
async def get_course(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Курс.
    """
    if len(message.text) != 1 or any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('Курс введен в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(course=message.text)
    await message.answer("Введите <b>Группу</b> в формате: <em>23/3</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.group)
async def get_group(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Группа.
    """
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


@dp.message_handler(state=Student.coursework)
async def get_coursework(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Курсовые.
    """
    if len(message.text.split()) > 200:
        await message.answer('Количество слов превышает допустимое значение - 200 слов', parse_mode='HTML')
        return
    await state.update_data(coursework=message.text)
    await message.answer(
        "Введите <b>Ваши знания</b> (при отсутствии введите: 'Нет') в формате: <em>Python, SQL, C++, JS</em>",
        parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.knowledge)
async def get_knowledge(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Знания.
    """
    if len(message.text.split()) > 200:
        await message.answer('Количество слов превышает допустимое значение - 200 слов', parse_mode='HTML')
        return
    await state.update_data(knowledge=message.text)
    data = await state.get_data()
    await message.answer(f"🧑‍💻<b>Ваши данные</b>\n\n"
                         f"<b>ФИО:</b> {data['student_name']}\n\n"
                         f"<b>Номер телефона:</b> <code>{data['phone']}</code>\n\n"
                         f"<b>ВУЗ:</b> {data['university']}\n\n"
                         f"<b>Факультет:</b> {data['faculty']}\n\n"
                         f"<b>Специальность:</b> {data['specialties']}\n\n"
                         f"<b>Кафедра:</b> {data['department']}\n\n"
                         f"<b>Курс:</b> {data['course']}\n\n"
                         f"<b>Группа:</b> {data['group']}\n\n"
                         f"<b>Курсовые:</b> {data['coursework']}\n\n"
                         f"<b>Знания:</b> {data['knowledge']}\n\n", parse_mode='HTML')
    student = registration_user(message.from_user.id, 'student', data)
    if student:
        await message.answer(f'Регистрация окончена.\n\n'
                             f'После рассмотрения заявки сотрудниками, вам придет уведомление.', parse_mode='HTML',
                             reply_markup=ikb_3)
    await state.finish()

