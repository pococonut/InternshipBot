from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboard import ikb, kb, ikb_2, ikb_3, change_ikb, change_ikb_2, back_ikb, back_cont_ikb, admin_ikb, task_ikb, \
    change_task_ikb, del_task_ikb, admin_ikb2, stud_ikb, change_stud_ikb, stud_appl_ikb, del_stud_ikb, stud_appl_ikb_2, \
    worker_ikb, task_worker_ikb, task_worker_own_ikb, student_task_show, student_task_choose, stud_is_approve, \
    student_task_choose_cont, student_task_already_choose, stud_reject_task
import string
from commands import register_student, select_user, user_type, change_stud_inform, select_employee, register_admin, \
    add_task, select_task, change_task, del_task, select_students, add_application, select_applications, \
    register_director, register_worker, select_worker_task, stud_approve, select_task_for_stud, select_already_get_stud
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeDefault
import re

TOKEN_API = ""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())  # инициализация входящих данных

commands = [
    types.BotCommand(command='/student', description='Меню студента'),
    types.BotCommand(command='/menu', description='Меню персонала'),
    types.BotCommand(command='/change', description='Изменение данных студента'),
    types.BotCommand(command='/show', description='Просмотр данных пользователя'),
]


async def set_commands(dp):
    await dp.bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats())


DESCRIPTION = "Данный телеграм бот предназначен для рабты с практиками и стажировками," \
              " с которыми можно ознакомиться после регистрации и подачи заявки."
FORM = """
Для подачи заявки необходиммо ввести такие данные как:

ФИО
ВУЗ
Факультет
Направление
Кафедра
Курс
Группа
Темы курсовых работ
Ваши знания

<b>отдельными сообщениями</b>.
"""


async def on_startup(_):
    print("Бот запущен")


# описание бота
@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer(DESCRIPTION)


"""# помощь
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND, parse_mode='HTML')"""


# старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать!\n\n" + DESCRIPTION)


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


@dp.message_handler(commands=['student'])
async def registration_command(message: types.Message):
    # await message.answer(text="Выберите опцию:", reply_markup=ikb)
    user_exist = user_type(message.from_user.id)
    usr = {'student': 'студент',
           'admin': 'администранор',
           'director': 'директор',
           'worker': 'сотрудник'}
    if not user_exist:
        await message.answer(FORM, parse_mode='HTML',
                             reply_markup=back_cont_ikb)
    else:
        keyboard = task_ikb
        if user_exist[0] == 'worker':
            keyboard = task_worker_ikb
        elif user_exist[0] == 'student':
            approve = stud_approve(message.from_user.id)
            if approve:
                keyboard = stud_is_approve
            else:
                keyboard = ikb_3
        print(user_exist[0])
        await message.answer(f'Вы зарегестрированы как <b>{usr.get(user_exist[0])}</b>.', parse_mode='HTML',
                             reply_markup=keyboard)


@dp.callback_query_handler(text='continue', state="*")
async def cont_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>",
                                     parse_mode='HTML', reply_markup=back_ikb)
    # await callback.message.edit_reply_markup()
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
        await state.update_data(student_name=" ".join([i.capitalize() for i in message.text.split()]))
        await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
        await Student.next()


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text.upper())
    await message.answer("Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text.capitalize())
    await message.answer("Введите <b>Направление</b> в формате: <em>Фундаментальные математика и механика</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text.capitalize())
    await message.answer("Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>",
                         parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text.upper())
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


# -------------------- Изменение параметров заявки студента --------------------


def chek_param(p, v):
    if p == 'student_name':
        if len(v.split()) != 3 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return " ".join([i.capitalize() for i in v.split()])
    elif p == 'university':
        if len(v.split()) != 1 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.upper()
    elif p == 'faculty':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.capitalize()
    elif p == 'specialties':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.capitalize()
    elif p == 'department':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.upper()
    elif p == 'course':
        if len(v) != 1 or any(chr.isalpha() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v
    elif p == 'group':
        if ((re.fullmatch('\d{,3}\D\d', v) is None) or ' ' in v or any(chr.isalpha() for chr in v) or any(
                chr in string.punctuation.replace('/', '') for chr in v)):
            return False
        else:
            return v
    else:
        return v


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
    elif u_type[0] == 'worker':
        await message.answer('Изменение данных доступно только для студентов.',
                             reply_markup=worker_ikb,
                             parse_mode='HTML')
    elif u_type[0] == 'admin' or u_type[0] == 'director':
        await message.answer('Изменение данных доступно только для студентов.',
                             reply_markup=admin_ikb,
                             parse_mode='HTML')
    else:
        await message.answer(f'Выберите параметр, который желаете изменить.', reply_markup=change_ikb)
        await Change_student.par.set()


@dp.callback_query_handler(text='change')
async def change_inline(callback: types.CallbackQuery):
    # await callback.message.edit_reply_markup()
    student_exist = select_user(callback.message.chat.id)
    if not student_exist:
        await callback.message.edit_text('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                         parse_mode='HTML')
    else:
        await callback.message.edit_text(f'Выберите параметр, который желаете изменить.', reply_markup=change_ikb)
        await Change_student.par.set()


@dp.callback_query_handler(text=stud_params, state=Change_student.par)
async def get_param_student(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(par=callback.data)
    s_p.append(callback.data)
    await callback.message.edit_text("Введите новое значение.", reply_markup=back_ikb)
    await Change_student.next()


@dp.message_handler(state=Change_student.new_val)
async def get_val_student(message: types.Message, state: FSMContext):
    x = chek_param(s_p[0], message.text)
    if not x:
        await message.answer("Значение введено в некорректном формате. Повторите ввод.")
        return
    s_p.clear()
    await state.update_data(new_val=x)
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

log_pass = {'admin': [['1', '111'], ['0', '000']],
            'director': [['2', '222'], ],
            'worker': [['3', '333'], ['4', '444']],
            }


@dp.message_handler(commands=['menu'])
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


def chek_wlogin(l, *args):
    f = False
    for i in args[0]:
        print(i)
        if i[0] == l:
            f = True
    return f


def chek_wpassword(p, *args):
    f = False
    for i in args[0]:
        if i[1] == p:
            f = True
    return f


@dp.message_handler(state=Authorisation.login)
async def get_login(message: types.Message, state=FSMContext):
    m = message.text
    if not chek_wlogin(m, log_pass.get('admin')) and not chek_wlogin(m, log_pass.get('director')) \
            and not chek_wlogin(m, log_pass.get('worker')):
        await message.answer("Введен неверный логин.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(login=message.text)
    await message.answer('Введите пароль.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.password)
async def get_login(message: types.Message, state=FSMContext):
    m = message.text
    if not chek_wpassword(m, log_pass.get('admin')) and not chek_wpassword(m, log_pass.get(
            'director')) and not chek_wpassword(m, log_pass.get('worker')):
        await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(password=message.text)
    await message.answer('Введите ФИО.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.name)
async def get_password(message: types.Message, state=FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    if chek_wlogin(data.get('login'), log_pass.get('admin')) and chek_wpassword(data.get('password'),
                                                                                log_pass.get('admin')):
        admin = register_admin(message.from_user.id, data)
        if admin:
            await message.answer('Вы авторизированны как <b>администатор</b>.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=admin_ikb)
    elif chek_wlogin(data.get('login'), log_pass.get('director')) and chek_wpassword(data.get('password'),
                                                                                     log_pass.get('director')):
        director = register_director(message.from_user.id, data)
        if director:
            await message.answer('Вы авторизированны как <b>директор</b>.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=admin_ikb)
    elif chek_wlogin(data.get('login'), log_pass.get('worker')) and chek_wpassword(data.get('password'),
                                                                                   log_pass.get('worker')):
        worker = register_worker(message.from_user.id, data)
        if worker:
            await message.answer('Вы авторизированны как <b>сотрудник</b>.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=worker_ikb)

    await state.finish()


# ------------------------- Добавление задачи -------------------------


class Task(StatesGroup):
    task_name = State()
    task_description = State()
    num_people = State()
    materials = State()


@dp.callback_query_handler(text='add_task')
async def add_t(callback: types.CallbackQuery):
    # await callback.message.edit_reply_markup()
    # await callback.message.delete()
    await callback.message.edit_text("Введите название задачи.", parse_mode='HTML', reply_markup=back_ikb)
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
                             reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)
        global page
        page = 0
    await state.finish()


# -------------------- Просмотр всех задач --------------------

page = 0


@dp.callback_query_handler(text='show_task')
async def show_task(callback: types.CallbackQuery):
    page = 0
    u_type = user_type(callback.from_user.id)[0]

    if u_type == 'student':
        tasks = select_task_for_stud()
        already_get = select_already_get_stud(callback.from_user.id)
        if already_get:
            keyboard = student_task_already_choose
        else:
            keyboard = student_task_choose
    else:
        tasks = select_task()
        keyboard = task_ikb
        if u_type == 'worker':
            keyboard = task_worker_ikb
    if not tasks:
        try:
            await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
        except:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент задач нет.\nЗагляните позже.',
                                          reply_markup=keyboard)
    else:
        count_tasks = len(tasks)
        await callback.message.edit_text(f"<b>№</b> {page + 1}/{count_tasks}\n\n"
                                         f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                         f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                         f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                         f"<b>Материалы:</b> {str(tasks[page].materials)}",
                                         parse_mode='HTML',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)


@dp.callback_query_handler(text='right')
async def right(callback: types.CallbackQuery):
    global page, page_s
    u_type = user_type(callback.from_user.id)[0]
    if u_type == 'student':
        tasks = select_task_for_stud()
        already_get = select_already_get_stud(callback.from_user.id)
        if already_get:
            keyboard = student_task_already_choose
        else:
            keyboard = student_task_choose
    else:
        tasks = select_task()
        keyboard = task_ikb
        if u_type == 'worker':
            keyboard = task_worker_ikb
    if not tasks:
        if u_type == 'student':
            keyboard = stud_is_approve
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
    else:
        count_tasks = len(tasks)
        page += 1
        if page == count_tasks:
            page = 0
        p_r = page
        if page <= -1:
            p_r = count_tasks + page
        print(page)
        await callback.message.edit_text(f"<b>№</b> {p_r + 1}/{count_tasks}\n\n"
                                         f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                         f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                         f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                         f"<b>Материалы:</b> {str(tasks[page].materials)}",
                                         parse_mode='HTML',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)


@dp.callback_query_handler(text='left')
async def left(callback: types.CallbackQuery):
    global page, page_s
    u_type = user_type(callback.from_user.id)[0]
    if u_type == 'student':
        tasks = select_task_for_stud()
        already_get = select_already_get_stud(callback.from_user.id)
        if already_get:
            keyboard = student_task_already_choose
        else:
            keyboard = student_task_choose
    else:
        tasks = select_task()
        keyboard = task_ikb
        if u_type == 'worker':
            keyboard = task_worker_ikb
    if not tasks:
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
    else:
        count_tasks = len(tasks)
        page -= 1
        p_l = 0
        if page == (-1) * count_tasks:
            page = 0
        if page <= -1:
            p_l = count_tasks
        await callback.message.edit_text(f"<b>№</b> {(p_l + page) + 1}/{count_tasks}\n\n"
                                         f"<b>Название:</b> {tasks[page].task_name}\n\n"
                                         f"<b>Описание:</b> {tasks[page].task_description}\n\n"
                                         f"<b>Количество людей:</b> {tasks[page].num_people}\n\n"
                                         f"<b>Материалы:</b> {str(tasks[page].materials)}", parse_mode='HTML',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)


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
    global page
    print("change", page + 1)
    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML',
                                  reply_markup=change_task_ikb)
    await Task_change.param.set()


@dp.callback_query_handler(text=ch_task_lst, state=Task_change.param)
async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(param=callback.data)
    u_type = user_type(callback.from_user.id)[0]
    await state.update_data(num_task=page)
    await callback.message.edit_text("Введите новое значение.")
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
    await message.answer('Задача изменена.', parse_mode='HTML',
                         reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)
    await state.finish()


# ---------------------- Удаление задачи ----------------------


class Task_del(StatesGroup):
    del_t = State()


@dp.callback_query_handler(text='del_task')
async def del_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    global page
    print("delite ", page + 1)
    await callback.message.answer('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await Task_del.del_t.set()


@dp.callback_query_handler(text='del_yes', state=Task_del.del_t)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(del_t=callback.data)
    tasks = select_task()
    u_type = user_type(callback.from_user.id)[0]
    t_id = tasks[page].task_id
    del_task(t_id)
    await state.finish()
    await callback.message.edit_text('Задача удалена', parse_mode='HTML',
                                     reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)


# -------------------- Просмотр задач сотрудника --------------------

page_w = 0


@dp.callback_query_handler(text='worker_task')
async def show_task(callback: types.CallbackQuery):
    global page_w
    page_w = 0
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    if not tasks:
        try:
            await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.',
                                             reply_markup=task_worker_own_ikb)
        except:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент задач нет.\nЗагляните позже.',
                                          reply_markup=task_worker_own_ikb)
    else:
        await callback.message.edit_text(f"<b>№</b> {page_w + 1}/{count_tasks}\n\n"
                                         f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                         f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                         f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                         f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                         reply_markup=task_worker_own_ikb, disable_web_page_preview=True)


@dp.callback_query_handler(text='worker_right')
async def right(callback: types.CallbackQuery):
    global page_w
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    page_w += 1
    if page_w == count_tasks:
        page_w = 0
    p_rw = page_w
    if page_w <= -1:
        p_rw = count_tasks + page_w
    await callback.message.edit_text(f"<b>№</b> {p_rw + 1}/{count_tasks}\n\n"
                                     f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                     f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                     f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                     f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                     reply_markup=task_worker_own_ikb, disable_web_page_preview=True)


@dp.callback_query_handler(text='worker_left')
async def left(callback: types.CallbackQuery):
    global page_w
    # await callback.message.edit_reply_markup()
    # await callback.message.delete()
    tasks = select_worker_task(callback.from_user.id)
    count_tasks = len(tasks)
    page_w -= 1
    p_lw = 0
    if page_w == (-1) * count_tasks:
        page_w = 0
    if page_w <= -1:
        p_lw = count_tasks
    await callback.message.edit_text(f"<b>№</b> {(p_lw + page_w) + 1}/{count_tasks}\n\n"
                                     f"<b>Название:</b> {tasks[page_w].task_name}\n\n"
                                     f"<b>Описание:</b> {tasks[page_w].task_description}\n\n"
                                     f"<b>Количество людей:</b> {tasks[page_w].num_people}\n\n"
                                     f"<b>Материалы:</b> {str(tasks[page_w].materials)}", parse_mode='HTML',
                                     reply_markup=task_worker_own_ikb, disable_web_page_preview=True)


# -------------------- Изменение параметров задачи сотрудника--------------------


class Task_change_w(StatesGroup):
    num_task = State()
    param = State()
    value = State()


@dp.callback_query_handler(text='change_task_w')
async def ch_task(callback: types.CallbackQuery):
    # num_task.append(page)
    await callback.message.edit_reply_markup()

    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML',
                                  reply_markup=change_task_ikb)
    await Task_change_w.param.set()


@dp.callback_query_handler(text=ch_task_lst, state=Task_change_w.param)
async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(param=callback.data)
    print("change!!!", page_w + 1)
    await state.update_data(num_task=page_w)
    await callback.message.edit_text("Введите новое значение.")
    await Task_change_w.next()


@dp.message_handler(state=Task_change_w)
async def ch_task_val(message: types.Message, state=FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b> {data['value']}\n\n", parse_mode='HTML')
    tasks = select_worker_task(message.from_user.id)
    t_id = tasks[data['num_task']].task_id
    print(t_id)
    change_task(t_id, data['param'][7:], data['value'])
    u_type = user_type(message.from_user.id)[0]
    await message.answer('Задача изменена.', parse_mode='HTML',
                         reply_markup=worker_ikb)
    await state.finish()


# ---------------------- Удаление задачи сотрудника ----------------------


class Task_del_w(StatesGroup):
    del_t = State()


@dp.callback_query_handler(text='del_task_w')
async def del_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await Task_del_w.del_t.set()


@dp.callback_query_handler(text='del_yes', state=Task_del_w.del_t)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(del_t=callback.data)
    tasks = select_worker_task(callback.from_user.id)
    print(tasks)
    print("delite ", page + 1)
    t_id = tasks[page_w].task_id
    del_task(t_id)
    u_type = user_type(callback.from_user.id)[0]
    await state.finish()
    await callback.message.edit_text('Задача удалена', parse_mode='HTML',
                                     reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)


# --------------------- Просмотр заявок студентов ---------------------

page_stud = 0


def print_stud(students, page_stud):
    s = f"""<b>ФИО:</b> {students[page_stud].student_name}\n
<b>ВУЗ:</b> {students[page_stud].university}\n
<b>Факультет:</b> {students[page_stud].faculty}\n
<b>Специальность:</b> {students[page_stud].specialties}\n
<b>Кафедра:</b> {students[page_stud].department}\n
<b>Курс:</b> {students[page_stud].course}\n
<b>Группа:</b> {students[page_stud].group}\n
<b>Курсовые:</b> {students[page_stud].coursework}\n
<b>Знания:</b> {students[page_stud].knowledge}\n
<b>Дата регистрации:</b> {students[page_stud].reg_date}\n"""
    return s


@dp.callback_query_handler(text='show_students')
async def show_stud(callback: types.CallbackQuery):
    # await callback.message.edit_reply_markup()
    # await callback.message.delete()
    page_stud = 0
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        u_type = user_type(callback.from_user.id)[0]
        try:
            await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.',
                                             reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)
        except Exception as e:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент заявок нет.\nЗагляните позже.',
                                          reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)
    else:
        try:
            await callback.message.edit_text(
                f"<b>№</b> {page_stud + 1}/{count_students}\n\n" + print_stud(students, page_stud),
                reply_markup=stud_appl_ikb, parse_mode='HTML')
        except Exception as e:
            print(page_stud)
            print(e)


@dp.callback_query_handler(text='right_stud')
async def std_right(callback: types.CallbackQuery):
    global page_stud
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        page_stud += 1
        if page_stud == count_students:
            page_stud = 0
        p_rs = page_stud
        if page_stud <= -1:
            p_rs = count_students + page_stud
        await callback.message.edit_text(f"<b>№</b> {p_rs + 1}/{count_students}\n\n" + print_stud(students, page_stud),
                                         reply_markup=stud_appl_ikb, parse_mode='HTML')


@dp.callback_query_handler(text='left_stud')
async def std_left(callback: types.CallbackQuery):
    global page_stud
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        page_stud -= 1
        p_ls = 0
        if page_stud == (-1) * count_students:
            page_stud = 0
        if page_stud <= -1:
            p_ls = count_students
        print(p_ls, page_stud)

        await callback.message.edit_text(
            f"<b>№</b> {(p_ls + page_stud) + 1}/{count_students}\n\n" + print_stud(students, page_stud),
            reply_markup=stud_appl_ikb, parse_mode='HTML')


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
    student_id = current_student(page_stud)
    add_application(student_id, callback.from_user.id, 1)
    try:
        await bot.send_message(student_id, 'Ваша заявка была <b>одобрена</b>.\n\nВы можете выбрать задачу из списка '
                                           'доступных задач.',
                               reply_markup=student_task_show, parse_mode='HTML')
        await callback.message.edit_text('Заявка одобрена.', reply_markup=stud_appl_ikb_2)
    except Exception as e:
        await callback.message.edit_text('ID студента не был найден.', reply_markup=stud_appl_ikb_2)


class Stud_del(StatesGroup):
    del_s = State()


@dp.callback_query_handler(text='reject')
async def reject_stud(callback: types.CallbackQuery):
    # await callback.message.edit_reply_markup()
    # await callback.message.delete()
    await callback.message.edit_text('Отклонить заявку?', parse_mode='HTML', reply_markup=del_stud_ikb)
    await Stud_del.del_s.set()


@dp.callback_query_handler(text='reject_yes', state=Stud_del.del_s)
async def reject_stud(callback: types.CallbackQuery, state=FSMContext):
    # await callback.message.edit_reply_markup()
    # await callback.message.delete()
    await state.update_data(del_s=callback.data)
    student_id = current_student(page_stud)
    add_application(student_id, callback.from_user.id, 0)
    await state.finish()
    try:
        await bot.send_message(student_id, 'Ваша заявка была <b>отклонена</b>.', parse_mode='HTML')
        await callback.message.edit_text('Заявка отклонена.', reply_markup=stud_appl_ikb_2)
    except Exception as e:
        await callback.message.edit_text('ID студента не был найден.', reply_markup=stud_appl_ikb_2)


# ----------------- Выбор задачи студентом -----------------


@dp.callback_query_handler(text='stud_get_task')
async def stud_get_task(callback: types.CallbackQuery):
    global page
    tasks = select_task_for_stud()
    t_id = tasks[page].task_id
    page = 0
    change_task(t_id, 'student_id', callback.from_user.id)
    await callback.message.edit_text('Задача выбрана.\nВы можете отказаться от задачи в разделе "Выбранные задачи".',
                                     reply_markup=student_task_choose_cont)


# ----------------- Просмотр выбранной студентом задачи -----------------


@dp.callback_query_handler(text='stud_chosen_tasks')
async def stud_get_task(callback: types.CallbackQuery):
    task = select_already_get_stud(callback.from_user.id)
    if not task:
        await callback.message.edit_text('Вы еще не выбрали задачу.', reply_markup=stud_is_approve)
    else:
        await callback.message.edit_text(f"<b>Выбранная задача:</b>\n\n"
                                         f"<b>Название:</b> {task.task_name}\n\n"
                                         f"<b>Описание:</b> {task.task_description}\n\n"
                                         f"<b>Количество людей:</b> {task.num_people}\n\n"
                                         f"<b>Материалы:</b> {str(task.materials)}",
                                         parse_mode='HTML',
                                         reply_markup=stud_reject_task,
                                         disable_web_page_preview=True)


# ----------------- Отображение информации студента\работника -----------------


@dp.callback_query_handler(text='show')
async def reg_callback(callback: types.CallbackQuery):
    s_id = int(callback.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        await callback.message.edit_text('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                         parse_mode='HTML')
    elif u_type[0] == 'student':
        await callback.message.edit_text(f"<b>Ваши данные</b>\n\n"
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
        await callback.message.edit_text(f"Ваши данные\n\n"
                                         f"<b>ФИО:</b> {user_show.name}\n\n", parse_mode='HTML')


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
                             f"<b>ФИО:</b> {user_show.name}\n\n", parse_mode='HTML')


# -------------------- Отмена действия --------------------


@dp.callback_query_handler(text='back', state="*")
async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    u_type = user_type(callback.from_user.id)

    if u_type is None:
        await callback.message.edit_text('Действие отменено.')
    elif u_type[0] == 'student':
        await callback.message.edit_text('Действие отменено.', reply_markup=ikb_3)
    else:
        await callback.message.edit_text('Действие отменено.',
                                         reply_markup=admin_ikb if u_type != 'worker' else worker_ikb)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)
