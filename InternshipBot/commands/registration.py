from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import dp
from db.commands import select_user, registration_user, get_user_type
from commands.general import check_user_parameter
from keyboard import back_cont_ikb, student_not_approved, back_ikb


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

    user_id = str(callback.from_user.id)
    user_exist = select_user(user_id)
    if user_exist:
        u_type = get_user_type(user_id)[0]
        await callback.message.edit_text(f"Вы уже зарегистрированы как {u_type}.")
        return

    await callback.message.edit_text(FORM, parse_mode='HTML', reply_markup=back_cont_ikb)


@dp.callback_query_handler(text='continue', state="*")
async def cont_command(callback: types.CallbackQuery):
    """
    Функция начала ввода параметров заявки.
    """

    msg_text = "Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>"
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=back_ikb)
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
        parameter = check_user_parameter("student_name", message.text)
        if not parameter:
            await message.answer('ФИО введено в некорректном формате')
            return

        msg_text = ("Введите <b>Номер телефона, привязанный к telegram</b> "
                    "в формате: <code><em>+79999999999</em></code>")
        await state.update_data(student_name=parameter)
        await message.answer(msg_text, parse_mode='HTML')
        await Student.next()


@dp.message_handler(state=Student.phone)
async def get_phone(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Номер телефона.
    """

    parameter = check_user_parameter("phone", message.text)
    if not parameter:
        await message.answer('Номер телефона введен в некорректном формате')
        return

    await state.update_data(phone=parameter)
    await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Университет.
    """

    parameter = check_user_parameter("university", message.text)
    if not parameter:
        await message.answer('ВУЗ введен в некорректном формате')
        return

    msg_text = "Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>"
    await state.update_data(university=parameter)
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Факультет.
    """

    parameter = check_user_parameter("faculty", message.text)
    if not parameter:
        await message.answer('Факультет введен в некорректном формате')
        return

    msg_text = "Введите <b>Направление</b> в формате: <em>Фундаментальные математика и механика</em>"
    await state.update_data(faculty=parameter)
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Специальность.
    """

    parameter = check_user_parameter("specialties", message.text)
    if not parameter:
        await message.answer('Направление введено в некорректном формате')
        return

    msg_text = "Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>"
    await state.update_data(specialties=message.text.capitalize())
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Кафедра.
    """

    parameter = check_user_parameter("department", message.text)
    if not parameter:
        await message.answer('Кафедра введена в некорректном формате')
        return

    msg_text = "Введите <b>Курс</b> в формате: <em>2</em>"
    await state.update_data(department=message.text.upper())
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.course)
async def get_course(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Курс.
    """

    parameter = check_user_parameter("course", message.text)
    if not parameter:
        await message.answer('Курс введен в некорректном формате')
        return

    msg_text = "Введите <b>Группу</b> в формате: <em>23/3</em>"
    await state.update_data(course=message.text)
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.group)
async def get_group(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Группа.
    """

    parameter = check_user_parameter("group", message.text)
    if not parameter:
        await message.answer('Группа введена в некорректном формате')
        return

    msg_text = ('Введите <b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате: '
                '<em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>')
    await state.update_data(group=message.text)
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.coursework)
async def get_coursework(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Курсовые.
    """

    parameter = check_user_parameter("coursework", message.text)
    if not parameter:
        await message.answer('Количество слов превышает допустимое значение - 200 слов')
        return

    msg_text = ("Введите <b>Ваши знания</b> (при отсутствии введите: "
                "'Нет') в формате: <em>Python, SQL, C++, JS</em>")
    await state.update_data(coursework=message.text)
    await message.answer(msg_text, parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.knowledge)
async def get_knowledge(message: types.Message, state=FSMContext):
    """
    Функция получения и проверки параметра заявки - Знания.
    """

    parameter = check_user_parameter("coursework", message.text)
    if not parameter:
        await message.answer('Количество слов превышает допустимое значение - 200 слов')
        return

    await state.update_data(knowledge=message.text)
    data = await state.get_data()
    student = registration_user(message.from_user.id, 'student', data)

    if student:
        msg_text = (f"🧑‍💻<b>Ваши данные</b>\n\n"
                    f"<b>ФИО:</b> {data['student_name']}\n"
                    f"<b>Номер телефона:</b> <code>{data['phone']}</code>\n"
                    f"<b>ВУЗ:</b> {data['university']}\n"
                    f"<b>Факультет:</b> {data['faculty']}\n"
                    f"<b>Специальность:</b> {data['specialties']}\n"
                    f"<b>Кафедра:</b> {data['department']}\n"
                    f"<b>Курс:</b> {data['course']}\n"
                    f"<b>Группа:</b> {data['group']}\n"
                    f"<b>Курсовые:</b> {data['coursework']}\n"
                    f"<b>Знания:</b> {data['knowledge']}\n\n"
                    f'Регистрация окончена.\n'
                    f'После рассмотрения заявки сотрудниками, вам придет уведомление.')
        await message.answer(msg_text, parse_mode='HTML', reply_markup=student_not_approved)
    await state.finish()

