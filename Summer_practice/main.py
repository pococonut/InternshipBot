from aiogram import Bot, Dispatcher, executor, types
from keyboard import ikb, kb, ikb_2, ikb_3, change_ikb, change_ikb_2, back_ikb, back_cont_ikb, admin_ikb, task_ikb, \
    change_task_ikb, del_task_ikb, admin_ikb2, stud_ikb, change_stud_ikb, stud_appl_ikb, del_stud_ikb, stud_appl_ikb_2, \
    worker_ikb, task_worker_ikb, task_worker_own_ikb
import string
from commands import register_student, select_user, user_type, change_stud_inform, select_employee, register_admin, \
    add_task, select_task, change_task, del_task, select_students, add_application, select_applications, \
    register_director, register_worker, select_worker_task
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import re

TOKEN_API = ""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())  # инициализация входящих данных

HELP_COMMAND = """
<b>/help</b> - список комманд\n
<b>/description</b> - описание бота\n
<b>/registration</b> - регистрация студента\n
<b>/change</b> - изменение данных студента\n
<b>/show</b> - просмотр данных пользователя\n
<b>/authorisation</b> - авторизация персонала\n
"""

DESCRIPTION = """
Данный телеграм бот предназначен для рабты с практиками и стажировками, с которыми можно ознакомиться после регистрации и подачи заявок
"""

FORM = """
Введите данные <b>отдельными сообщениями</b>.

<b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>

<b>ВУЗ</b> в формате: <em>КУБГУ</em>

<b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>

<b>Направление</b> в формате: <em>Математика и компьютерные науки</em>

<b>Кафедра</b> (при отсутствии введите: "Нет") в формате: <em>ВМИ</em>

<b>Курс</b> в формате: <em>2</em>

<b>Группа</b> в формате: <em>23/3</em>

<b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате: <em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>

<b>Ваши знания</b> (при отсутствии введите: "Нет") в формате: <em>Python, SQL, C++, JS</em>
"""


async def on_startup(_):
    print("Бот запущен")


# описание бота
@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer(DESCRIPTION)


# помощь
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND, parse_mode='HTML')


# старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Добро пожаловать!",
                         reply_markup=kb)


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


@dp.message_handler(commands=['registration'])
async def registration_command(message: types.Message):
    # await message.answer(text="Выберите опцию:", reply_markup=ikb)
    user_exist = user_type(message.from_user.id)
    usr = {'student': 'студент',
           'admin': 'администранор',
           'director': 'директор',
           'worker': 'сотрудник'}
    if user_exist and user_exist[0] != 'student':
        print(user_exist[0])
        await message.answer(f'Вы уже зарегестрированы как {usr.get(user_exist[0])}.', parse_mode='HTML',
                             reply_markup=admin_ikb if user_exist[0] != 'worker' else worker_ikb)
        # await message.edit_reply_markup()
    elif user_exist and user_exist[0] == 'student':
        await message.answer(f'Вы уже зарегестрированы как {usr.get(user_exist[0])}.', parse_mode='HTML',
                             reply_markup=stud_ikb)
    else:
        await message.answer("Введите данные <b>отдельными сообщениями</b>.", parse_mode='HTML',
                             reply_markup=back_cont_ikb)


@dp.callback_query_handler(text='continue', state="*")
async def cont_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>", parse_mode='HTML')
    await callback.message.edit_reply_markup()
    await Student.student_name.set()


@dp.message_handler(state=Student.student_name)
async def get_student_name(message: types.Message, state: FSMContext):
    student_exist = select_user(message.from_user.id)
    if student_exist:
        await state.finish()
        await state.reset_state(with_data=False)
    else:
        if len(message.text.split()) != 3 or any(chr.isdigit() for chr in message.text) or any(
                chr in string.punctuation for chr in message.text):
            await message.answer('ФИО введено в некорректом формате', parse_mode='HTML')
            return
        await state.update_data(student_name=message.text)
        await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
        await Student.next()


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text)
    await message.answer("Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text)
    await message.answer("Введите <b>Направление</b> в формате: <em>Математика и компьютерные науки</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text)
    await message.answer("Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text)
    await message.answer("Введите <b>Курс</b> в формате: <em>2</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.course)
async def get_course(message: types.Message, state=FSMContext):
    if len(message.text) != 1 or any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('Курс введен в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(course=message.text)
    await message.answer("Введите <b>Группу</b> в формате: <em>23/3</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.group)
async def get_group(message: types.Message, state=FSMContext):
    if (re.fullmatch('\d{,3}\D\d', message.text) is None) or any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation.replace('/', '') for chr in message.text) or ' ' in message.text:
        await message.answer('Группа введена в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(group=message.text)
    await message.answer(
        'Введите <b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате: <em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>',
        parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.coursework)
async def get_coursework(message: types.Message, state=FSMContext):
    await state.update_data(coursework=message.text)
    await message.answer(
        "Введите <b>Ваши знания</b> (при отсутствии введите: 'Нет') в формате: <em>Python, SQL, C++, JS</em>",
        parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.knowledge)
async def get_knowledge(message: types.Message, state=FSMContext):
    await state.update_data(knowledge=message.text)
    data = await state.get_data()
    await message.answer(f"Ваши данные\n\n"
                         f"ФИО: {data['student_name']}\n\n"
                         f"ВУЗ: {data['university']}\n\n"
                         f"Факультет: {data['faculty']}\n\n"
                         f"Специальность: {data['specialties']}\n\n"
                         f"Кафедра: {data['department']}\n\n"
                         f"Курс: {data['course']}\n\n"
                         f"Группа: {data['group']}\n\n"
                         f"Курсовые: {data['coursework']}\n\n"
                         f"Знания: {data['knowledge']}\n\n")
    student = register_student(message.from_user.id, data)
    if student:
        await message.answer(f'Регистрация окончена.\n\n'
                             f'После рассмотрения заявки сотрудниками, вам придет уведомление.', parse_mode='HTML',
                             reply_markup=ikb_3)
    await state.finish()


# -------------------- Изменение параметров заявки студента --------------------


def chek_param(p, v):
    if p == 'student_name' and (
            len(v.split()) != 3 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'university' and (
            len(v.split()) != 1 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'faculty' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'specialties' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'department' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'course' and (
            len(v) != 1 or any(chr.isalpha() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == 'group' and (
            (re.fullmatch('\d{,3}\D\d', v) is None) or ' ' in v or any(chr.isalpha() for chr in v) or any(
            chr in string.punctuation.replace('/', '') for chr in v)):
        return False

    return True


class Change_student(StatesGroup):
    par = State()
    new_val = State()


chek_d = {'student_name': 'ФИО',
          'university': 'ВУЗ',
          'faculty': 'Факультет',
          'specialties': 'Направление',
          'department': 'Кафедра',
          'course': 'Курс',
          'group': 'Группа',
          'coursework': 'Курсовые работы',
          'knowledge': 'Знания',
          }

stud_params, s_p = ['student_name', 'university', 'faculty', 'specialties',
                    'department', 'course', 'group', 'coursework', 'knowledge'], []


@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    u_type = user_type(message.from_user.id)
    student_exist = select_user(message.from_user.id)
    if not student_exist:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    elif u_type[0] != 'student':
        await message.answer('Изменение данных доступно только для студентов.', parse_mode='HTML')
    else:
        await message.answer(f'Выберите параметр, который желаете изменить.', reply_markup=change_ikb)
        await Change_student.par.set()


@dp.callback_query_handler(text='change')
async def change_inline(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    u_type = user_type(callback.message.chat.id)
    student_exist = select_user(callback.message.chat.id)
    if not student_exist:
        await callback.message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                      parse_mode='HTML')
    elif u_type[0] != 'student':
        await callback.message.answer('Изменение данных доступно только для студентов.', parse_mode='HTML')
    else:
        await callback.message.answer(f'Выберите параметр, который желаете изменить.', reply_markup=change_ikb)
        await Change_student.par.set()


@dp.callback_query_handler(text=stud_params, state=Change_student.par)
async def get_param_student(callback: types.CallbackQuery, state=FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await state.update_data(par=callback.data)
    s_p.append(callback.data)
    await callback.message.answer("Введите новое значение.")
    await Change_student.next()


@dp.message_handler(state=Change_student.new_val)
async def get_val_student(message: types.Message, state: FSMContext):
    if not chek_param(s_p[0], message.text):
        await message.answer("Значение введено в некорректном формате. Повторите ввод.")
        return
    s_p.clear()
    await state.update_data(new_val=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {chek_d.get(data['par'])}\n\n"
                         f"<b>Новое значение:</b> {data['new_val']}", parse_mode='HTML')

    change_stud_inform(message.from_user.id, data['par'], data['new_val'])
    await message.answer('Параметр изменен.', parse_mode='HTML', reply_markup=ikb_3)  # reply_markup=ikb_2
    await state.finish()


# ------------------- Регистрация сотрудников -------------------


class Authorisation(StatesGroup):
    login = State()
    password = State()
    name = State()


authorisation_lst = []

log_pass = {'admin': ['1', '111'],
            'director': ['2', '222'],
            'worker': [['3', '333'], ['4', '444']],
            }


@dp.message_handler(commands=['authorisation'])
async def registration_command(message: types.Message):
    # await message.answer(text="Выберите опцию:", reply_markup=ikb)
    u_type = user_type(message.from_user.id)
    print(u_type)

    if u_type is None:
        await message.answer(f'Введите логин.', parse_mode='HTML', reply_markup=back_ikb)
        await Authorisation.login.set()
    elif u_type[0] == 'admin':
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=admin_ikb)
    elif u_type[0] == 'director':
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=admin_ikb)
    elif u_type[0] == 'worker':
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=worker_ikb)
    elif u_type[0] == 'student':
        await message.answer("Вы не являетесь сотрудником.", parse_mode='HTML')


@dp.message_handler(state=Authorisation.login)
async def get_login(message: types.Message, state=FSMContext):
    if message.text != log_pass.get('admin')[0] and message.text != log_pass.get('director')[0] and message.text != \
            log_pass.get('worker')[0][0] and message.text != log_pass.get('worker')[1][0]:
        await message.answer("Введен неверный логин.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(login=message.text)
    await message.answer('Введите пароль.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.password)
async def get_login(message: types.Message, state=FSMContext):
    if message.text != log_pass.get('admin')[1] and message.text != log_pass.get('director')[1] and message.text != \
            log_pass.get('worker')[0][1] and message.text != log_pass.get('worker')[1][1]:
        await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(password=message.text)
    await message.answer('Введите ФИО.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.name)
async def get_password(message: types.Message, state=FSMContext):
    # if message.text != log_pass.get('admin')[1]:
    #    await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
    #   return
    await state.update_data(name=message.text)
    data = await state.get_data()
    # await message.answer(f'login: {data["login"]}\npassword: {data["password"]}')
    # student = register_student(message.from_user.id, data)
    if data.get('login') == log_pass.get('admin')[0] and data.get('password') == log_pass.get('admin')[1]:
        admin = register_admin(message.from_user.id, data)
        if admin:
            await message.answer('Вы авторизированны как администатор.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=admin_ikb)
    elif data.get('login') == log_pass.get('director')[0] and data.get('password') == log_pass.get('director')[1]:
        director = register_director(message.from_user.id, data)
        if director:
            await message.answer('Вы авторизированны как директор.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=admin_ikb)
    elif data.get('login') == log_pass.get('worker')[0][0] and data.get('password') == log_pass.get('worker')[0][1]:
        worker = register_worker(message.from_user.id, data)
        if worker:
            await message.answer('Вы авторизированны как сотрудник.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=worker_ikb)
    elif data.get('login') == log_pass.get('worker')[1][0] and data.get('password') == log_pass.get('worker')[1][1]:
        worker = register_worker(message.from_user.id, data)
        if worker:
            await message.answer('Вы авторизированны как сотрудник.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=worker_ikb)
        else:
            print(worker)

    await state.finish()


# ------------------------- Добавление задачи -------------------------


class Task(StatesGroup):
    task_name = State()
    task_description = State()
    num_people = State()
    materials = State()


@dp.callback_query_handler(text='add_task')
async def add_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("Введите название задачи.", parse_mode='HTML', reply_markup=back_ikb)
    await Task.task_name.set()


@dp.message_handler(state=Task.task_name)
async def add_task_name(message: types.Message, state=FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer('Введите описание задачи.')
    await Task.next()


@dp.message_handler(state=Task.task_description)
async def add_task_description(message: types.Message, state=FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer('Введите количество человек.')
    await Task.next()


@dp.message_handler(state=Task.num_people)
async def add_task_num_people(message: types.Message, state=FSMContext):
    await state.update_data(num_people=message.text)
    await message.answer('Введите материалы.')
    await Task.next()


@dp.message_handler(state=Task.materials)
async def add_task_materials(message: types.Message, state=FSMContext):
    await state.update_data(materials=str(message.text))
    data = await state.get_data()
    task = add_task(message.from_id, data)
    u_type = user_type(message.from_user.id)[0]
    if task:
        await message.answer(f'<b>Добавлена задача:</b>\n\n'
                             f'<b>Название:</b> {data["task_name"]}\n\n'
                             f'<b>Описание:</b> {data["task_description"]}\n\n'
                             f'<b>Количество людей:</b> {data["num_people"]}\n\n'
                             f'<b>Материалы:</b> {str(data["materials"])}', parse_mode='HTML',
                             reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)
    await state.finish()


# -------------------- Просмотр всех задач --------------------

page = 0


@dp.callback_query_handler(text='show_task')
async def show_task(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    tasks = select_task()
    count_tasks = len(tasks)
    u_type = user_type(callback.from_user.id)[0]
    if not tasks:
        await callback.message.answer('В данный момент задач нет.\nЗагляните позже.',
                                      reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)
    else:
        await callback.message.answer(f"<b>№</b> {page + 1}/{count_tasks}\n\n"
                                      f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                      f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                      f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                      f"<b>Материалы:</b> {str(tasks[page].materials)}", parse_mode='HTML',
                                      reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='right')
async def right(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    global page
    tasks = select_task()
    count_tasks = len(tasks)
    page += 1
    if page == count_tasks:
        page = 0
    u_type = user_type(callback.from_user.id)[0]
    await callback.message.answer(f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                  f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                  f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                  f"<b>Материалы:</b> {str(tasks[page].materials)}", parse_mode='HTML',
                                  reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='left')
async def left(callback: types.CallbackQuery):
    global page
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    tasks = select_task()
    count_tasks = len(tasks)
    page -= 1
    if page == (-1) * count_tasks:
        page = 0
    u_type = user_type(callback.from_user.id)[0]
    await callback.message.answer(f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                  f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                  f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                  f"<b>Материалы:</b> {str(tasks[page].materials)}", parse_mode='HTML',
                                  reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)


# f"<b>№</b> {(page - count_tasks) + 1}/{count_tasks}\n\n"

# -------------------- Просмотр задач сотрудника --------------------
# worker_task

page_w = 0

@dp.callback_query_handler(text='worker_task')
async def show_task(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    await callback.message.answer(f"<b>№</b> {page_w + 1}/{count_tasks}\n\n"
                                  f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                  f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                  f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                  f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                  reply_markup=task_worker_own_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='worker_right')
async def right(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    global page_w
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    page_w += 1
    if page_w == count_tasks:
        page_w = 0
    u_type = user_type(callback.from_user.id)[0]
    await callback.message.answer(f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                  f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                  f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                  f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                  reply_markup=task_worker_own_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='worker_left')
async def left(callback: types.CallbackQuery):
    global page_w
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    page_w -= 1
    if page_w == (-1) * count_tasks:
        page_w = 0
    u_type = user_type(callback.from_user.id)[0]
    await callback.message.answer(f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                  f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                  f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                  f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                  reply_markup=task_worker_own_ikb)


# -------------------- Изменение параметров задачи --------------------


class Task_change(StatesGroup):
    num_task = State()
    param = State()
    value = State()


param_task = {'change_task_name': 'Название',
              'change_task_description': 'Описание',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

ch_task_lst = ['change_task_name', 'change_task_description', 'change_num_people', 'change_materials']


@dp.callback_query_handler(text='change_task')
async def ch_task(callback: types.CallbackQuery):
    # num_task.append(page)
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML',
                                  reply_markup=change_task_ikb)
    await Task_change.param.set()


@dp.callback_query_handler(text=ch_task_lst, state=Task_change.param)
async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await state.update_data(param=callback.data)
    await state.update_data(num_task=page)
    await callback.message.answer("Введите новое значение.")
    await Task_change.next()


@dp.message_handler(state=Task_change)
async def ch_task_val(message: types.Message, state=FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b> {data['value']}\n\n", parse_mode='HTML')
    tasks = select_task()
    t_id = tasks[data['num_task']].task_id
    change_task(t_id, data['param'][7:], data['value'])
    u_type = user_type(message.from_user.id)[0]
    await message.answer('Задача изменена.', parse_mode='HTML', reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)
    await state.finish()


# ---------------------- Удаление задачи ----------------------


class Task_del(StatesGroup):
    del_t = State()


@dp.callback_query_handler(text='del_task')
async def del_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await Task_del.del_t.set()


@dp.callback_query_handler(text='del_yes', state=Task_del.del_t)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await state.update_data(del_t=callback.data)
    tasks = select_task()
    print(page)
    t_id = tasks[page].task_id
    print(t_id)
    del_task(t_id)
    u_type = user_type(callback.from_user.id)[0]
    await state.finish()
    await callback.message.answer('Задача удалена', parse_mode='HTML', reply_markup=task_ikb if u_type != 'worker' else task_worker_ikb)


# --------------------- Просмотр заявок студентов ---------------------

page_stud = 0


def print_stud(students, page_stud):
    s = f"""ФИО: {students[page_stud].student_name}\n
ВУЗ: {students[page_stud].university}\n
Факультет: {students[page_stud].faculty}\n
Специальность: {students[page_stud].specialties}\n
Кафедра: {students[page_stud].department}\n
Курс: {students[page_stud].course}\n
Группа: {students[page_stud].group}\n
Курсовые: {students[page_stud].coursework}\n
Знания: {students[page_stud].knowledge}\n
Дата регистрации: {students[page_stud].reg_date}\n"""
    return s


@dp.callback_query_handler(text='show_students')
async def show_stud(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    page_stud = 0
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        u_type = user_type(callback.from_user.id)[0]
        await callback.message.answer('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)
    else:
        await callback.message.answer(print_stud(students, page_stud), reply_markup=stud_appl_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='right_stud')
async def std_right(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    global page_stud
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.answer('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        page_stud += 1
        if page_stud >= count_students:
            page_stud = 0
        await callback.message.answer(print_stud(students, page_stud), reply_markup=stud_appl_ikb)


# f"<b>№</b> {page+1}/{count_tasks}\n\n"


@dp.callback_query_handler(text='left_stud')
async def std_left(callback: types.CallbackQuery):
    global page_stud
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.answer('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        print(page_stud, count_students)
        page_stud -= 1
        if page_stud <= (-1) * count_students:
            page_stud = 0
        await callback.message.answer(print_stud(students, page_stud), reply_markup=stud_appl_ikb)


# ---------------------- Принятие\отклонение заявки ----------------------


def current_student(page_s):
    all_students = select_students()
    applications = select_applications()
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    student_id = students[page_s].telegram_id
    print(page_s, student_id, students[page_s].student_name)
    return student_id


@dp.callback_query_handler(text='approve')
async def approve_stud(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    student_id = current_student(page_stud)
    add_application(student_id, callback.from_user.id, 1)

    await callback.message.answer('Заявка одобрена.', reply_markup=stud_appl_ikb_2)


class Stud_del(StatesGroup):
    del_s = State()


@dp.callback_query_handler(text='reject')
async def reject_stud(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer('Отклонить заявку?', parse_mode='HTML', reply_markup=del_stud_ikb)
    await Stud_del.del_s.set()


@dp.callback_query_handler(text='reject_yes', state=Stud_del.del_s)
async def reject_stud(callback: types.CallbackQuery, state=FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await state.update_data(del_s=callback.data)
    student_id = current_student(page_stud)
    add_application(student_id, callback.from_user.id, 0)
    await state.finish()
    await callback.message.answer('Заявка отклонена.', reply_markup=stud_appl_ikb_2)


# ----------------- Отображение информации студента\работника -----------------


@dp.callback_query_handler(text='show')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        await callback.message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                      parse_mode='HTML')
    elif u_type[0] == 'student':
        await callback.message.answer(f"<b>Ваши данные</b>\n\n"
                                      f"<b>ФИО:</b> {user_show.student_name}\n\n"
                                      f"<b>ВУЗ:</b> {user_show.university}\n\n"
                                      f"<b>Факультет:</b> {user_show.faculty}\n\n"
                                      f"<b>Направление:</b> {user_show.specialties}\n\n"
                                      f"<b>Кафедра:</b> {user_show.department}\n\n"
                                      f"<b>Курс:</b> {user_show.course}\n\n"
                                      f"<b>Группа:</b> {user_show.group}\n\n"
                                      f"<b>Курсовые:</b> {user_show.coursework}\n\n"
                                      f"<b>Знания:</b> {user_show.knowledge}\n\n"
                                      f"<b>Дата регистрации:</b> {user_show.reg_date}\n\n",
                                      parse_mode='HTML',
                                      reply_markup=change_stud_ikb
                                      )
    else:
        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.name}\n\n")


@dp.message_handler(commands=['show'])
async def show_params(message: types.Message):
    s_id = int(message.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                             parse_mode='HTML')
    elif u_type[0] == 'student':
        await message.answer(f"<b>Ваши данные</b>\n\n"
                             f"<b>ФИО:</b> {user_show.student_name}\n\n"
                             f"<b>ВУЗ:</b> {user_show.university}\n\n"
                             f"<b>Факультет:</b> {user_show.faculty}\n\n"
                             f"<b>Направление:</b> {user_show.specialties}\n\n"
                             f"<b>Кафедра:</b> {user_show.department}\n\n"
                             f"<b>Курс:</b> {user_show.course}\n\n"
                             f"<b>Группа:</b> {user_show.group}\n\n"
                             f"<b>Курсовые:</b> {user_show.coursework}\n\n"
                             f"<b>Знания:</b> {user_show.knowledge}\n\n"
                             f"<b>Дата регистрации:</b> {user_show.reg_date}\n\n",
                             parse_mode='HTML',
                             reply_markup=change_stud_ikb
                             )
    else:
        await message.answer(f"Ваши данные\n\n"
                             f"ФИО: {user_show.name}\n\n")


# -------------------- Отмена действия --------------------


@dp.callback_query_handler(text='back', state="*")
async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer('Действие отменено.')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
