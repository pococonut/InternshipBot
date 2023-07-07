from aiogram import Bot, Dispatcher, executor, types
from keyboard import ikb, kb, ikb_2, ikb_3, change_ikb, change_ikb_2, back_ikb, back_cont_ikb, admin_ikb, task_ikb
import string
from commands import register_student, select_user, user_type, change_stud_inform, select_employee, register_admin, add_task, select_task
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

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
    if user_exist:
        await message.answer(f'Вы уже зарегестрированы как {usr.get(user_exist[0])}.', parse_mode='HTML', reply_markup=ikb_3)
        #await message.edit_reply_markup()
    else:
        await message.answer("Введите данные <b>отдельными сообщениями</b>.", parse_mode='HTML', reply_markup=back_cont_ikb)



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
            await message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
            return
        await state.update_data(student_name=message.text)
        await message.answer("Введите <b>ВУЗ</b> в формате: <em>КУБГУ</em>", parse_mode='HTML')
        await Student.next()


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text)
    await message.answer("Введите <b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text)
    await message.answer("Введите <b>Направление</b> в формате: <em>Математика и компьютерные науки</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text)
    await message.answer("Введите <b>Кафедру</b> (при отсутствии введите: 'Нет') в формате: <em>ВМИ</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text)
    await message.answer("Введите <b>Курс</b> в формате: <em>2</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.course)
async def get_course(message: types.Message, state=FSMContext):
    if any(chr.isalpha() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Курс введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(course=message.text)
    await message.answer("Введите <b>Группу</b> в формате: <em>23/3</em>", parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.group)
async def get_group(message: types.Message, state=FSMContext):
    if any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation.replace('./', '') for chr in message.text):
        await message.answer('Группа введена в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(group=message.text)
    await message.answer('Введите <b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате: <em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>', parse_mode='HTML')
    await Student.next()


@dp.message_handler(state=Student.coursework)
async def get_coursework(message: types.Message, state=FSMContext):
    await state.update_data(coursework=message.text)
    await message.answer("Введите <b>Ваши знания</b> (при отсутствии введите: 'Нет') в формате: <em>Python, SQL, C++, JS</em>", parse_mode='HTML')
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
        await message.answer('Регистрация окончена.', parse_mode='HTML', reply_markup=ikb_2)
    await state.finish()


class Authorisation(StatesGroup):
    login = State()
    password = State()
    name = State()


authorisation_lst = []

log_pass = {'admin': ['1', '111']}


@dp.message_handler(commands=['authorisation'])
async def registration_command(message: types.Message):
    # await message.answer(text="Выберите опцию:", reply_markup=ikb)
    u_type = user_type(message.from_user.id)
    print(u_type)

    if u_type is None:
        #admin_exist = select_employee(message.from_user.id)
        #if admin_exist:
        #await message.answer(f'Здравствуйте, {" ".join(admin_exist[0][0].split()[1:])}.\nВведите логин.', parse_mode='HTML', reply_markup=back_ikb)
        await message.answer(f'Введите логин.', parse_mode='HTML', reply_markup=back_ikb)
        #print(admin_exist[1][0], admin_exist[2][0])
        #authorisation_lst.append(admin_exist[1][0])
        #authorisation_lst.append(admin_exist[2][0])
        await Authorisation.login.set()
    elif u_type[0] == 'admin':
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=admin_ikb)
    elif u_type[0] == 'student':
        await message.answer("Вы не являетесь сотрудником.", parse_mode='HTML')


@dp.message_handler(state=Authorisation.login)
async  def get_login(message: types.Message, state=FSMContext):
    if message.text != log_pass.get('admin')[0]:
        await message.answer("Введен неверный логин.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(login=message.text)
    await message.answer('Введите пароль.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.password)
async  def get_login(message: types.Message, state=FSMContext):
    if message.text != log_pass.get('admin')[1]:
        await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(password=message.text)
    await message.answer('Введите ФИО.')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.name)
async def get_password(message: types.Message, state=FSMContext):
    #if message.text != log_pass.get('admin')[1]:
    #    await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
    #   return
    await state.update_data(name=message.text)
    data = await state.get_data()
    #await message.answer(f'login: {data["login"]}\npassword: {data["password"]}')
    #student = register_student(message.from_user.id, data)
    if data.get('login') == log_pass.get('admin')[0] and data.get('password') == log_pass.get('admin')[1]:
        admin = register_admin(message.from_user.id, data)
        if admin:
            await message.answer('Вы авторизированны как администатор.', parse_mode='HTML')
            await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=admin_ikb)

    await state.finish()


class Task(StatesGroup):
    task_name = State()
    task_description = State()
    num_people = State()
    materials = State()


@dp.callback_query_handler(text='add_task')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("Введите название задачи.", parse_mode='HTML', reply_markup=back_ikb)
    await Task.task_name.set()


@dp.message_handler(state=Task.task_name)
async def get_login(message: types.Message, state=FSMContext):

    await state.update_data(task_name=message.text)
    await message.answer('Введите описание задачи.')
    await Task.next()


@dp.message_handler(state=Task.task_description)
async  def get_login(message: types.Message, state=FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer('Введите количество человек.')
    await Task.next()


@dp.message_handler(state=Task.num_people)
async  def get_login(message: types.Message, state=FSMContext):
    await state.update_data(num_people=message.text)
    await message.answer('Введите материалы.')
    await Task.next()


@dp.message_handler(state=Task.materials)
async def get_password(message: types.Message, state=FSMContext):

    await state.update_data(materials=message.text)
    data = await state.get_data()
    task = add_task(data)
    if task:
        await message.answer(f'Добавлена задача:\n\n'
                             f'Название: {data["task_name"]}\n\n'
                             f'Описание: {data["task_description"]}\n\n'
                             f'Количество людей: {data["num_people"]}\n\n'
                             f'Материалы: {data["materials"]}')
    await state.finish()


@dp.callback_query_handler(text='show_task')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    tasks = select_task()
    count_tasks = len(tasks)


    print(count_tasks)
    await callback.message.answer(f"Название: {tasks[0].task_name}\n\n"
                                  f"Описание: {tasks[0].task_description}\n\n"
                                  f"Количество людей: {tasks[0].num_people}\n\n"
                                  f"Материалы: {tasks[0].materials}", parse_mode='HTML', reply_markup=task_ikb)

page = 0
@dp.callback_query_handler(text='right')
async def reg_callback(callback: types.CallbackQuery):
    global page
    tasks = select_task()
    count_tasks = len(tasks)
    page += 1
    await callback.message.answer(f"Название: {tasks[page].task_name}\n\n"
                                  f"Описание: {tasks[page].task_description}\n\n"
                                  f"Количество людей: {tasks[page].num_people}\n\n"
                                  f"Материалы: {tasks[page].materials}", parse_mode='HTML', reply_markup=task_ikb)



@dp.callback_query_handler(text='show')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type[0] == 'student':
        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.student_name}\n\n"
                                      f"ВУЗ: {user_show.university}\n\n"
                                      f"Факультет: {user_show.faculty}\n\n"
                                      f"Специальность: {user_show.specialties}\n\n"
                                      f"Кафедра: {user_show.department}\n\n"
                                      f"Курс: {user_show.course}\n\n"
                                      f"Группа: {user_show.group}\n\n"
                                      f"Курсовые: {user_show.coursework}\n\n"
                                      f"Знания: {user_show.knowledge}\n\n"
                                      f"Дата регистрации: {user_show.reg_date}\n\n"
                                      )
    elif u_type[0] != 'student':
        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.name}\n\n")
    else:
        await callback.message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                      parse_mode='HTML')


@dp.message_handler(commands=['show'])
async def show_params(message: types.Message):
    s_id = int(message.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type[0] == 'student':
        await message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.student_name}\n\n"
                                      f"ВУЗ: {user_show.university}\n\n"
                                      f"Факультет: {user_show.faculty}\n\n"
                                      f"Специальность: {user_show.specialties}\n\n"
                                      f"Кафедра: {user_show.department}\n\n"
                                      f"Курс: {user_show.course}\n\n"
                                      f"Группа: {user_show.group}\n\n"
                                      f"Курсовые: {user_show.coursework}\n\n"
                                      f"Знания: {user_show.knowledge}\n\n"
                                      f"Дата регистрации: {user_show.reg_date}\n\n"
                                      )
    elif u_type[0] != 'student':
        await message.answer(f"Ваши данные\n\n"
                             f"ФИО: {user_show.name}\n\n")
    else:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                      parse_mode='HTML')

def chek_param(p, v):
    if p == '1' and (
            len(v.split()) != 3 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '2' and (
            len(v.split()) != 1 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '3' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '4' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '5' and (any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '6' and (any(chr.isalpha() for chr in v) or any(chr in string.punctuation for chr in v)):
        return False
    elif p == '7' and (
            any(chr.isalpha() for chr in v) or any(chr in string.punctuation.replace('./', '') for chr in v)):
        return False

    return True


class Change_student(StatesGroup):
    param = State()
    new_val = State()


change_d, chek_d = {}, {'1': ['student_name', 'ФИО'],
                        '2': ['university', 'ВУЗ'],
                        '3': ['faculty', 'Факультет'],
                        '4': ['specialties', 'Направление'],
                        '5': ['department', 'Кафедра'],
                        '6': ['course', 'Курс'],
                        '7': ['group', 'Группа'],
                        '8': ['coursework', 'Курсовые работы'],
                        '9': ['knowledge', 'Знания'],
                        }


@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    u_type = user_type(message.from_user.id)
    print(u_type)
    student_exist = select_user(message.from_user.id)
    if not student_exist:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    elif u_type[0] != 'student':
        await message.answer('Изменение данных доступно только для студентов.', parse_mode='HTML')
    else:
        await message.answer(f'Введите номер параметра, который желаете изменить:\n\n'
                             f'ФИО - 1\n\n'
                             f'ВУЗ - 2\n\n'
                             f'Факультет - 3\n\n'
                             f'Направление - 4\n\n'
                             f'Кафедра - 5\n\n'
                             f'Курс - 6\n\n'
                             f'Группа - 7\n\n'
                             f'Темы курсовых работ - 8\n\n'
                             f'Ваши знания - 9\n\n',
                             reply_markup=back_ikb
                             )
        await Change_student.param.set()


@dp.callback_query_handler(text='back', state="*")
async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer('Действие отменено.')


@dp.message_handler(state=Change_student.param)
async def get_param(message: types.Message, state=FSMContext):
    if message.text not in chek_d:
        await message.answer("Вы ввели неверный параметр.\nПожалуйста, повторите ввод.")
        return
    change_d['p'] = message.text
    print(message.text)
    await state.update_data(param=message.text)
    await message.answer("Введите новое значение.")
    await Change_student.next()


@dp.message_handler(state=Change_student.new_val)
async def get_val(message: types.Message, state: FSMContext):
    if chek_param(change_d['p'], message.text) is False:
        await message.answer("Вы ввели значение в некоректном  формате.\n\n Пожалуйста, повторите ввод.")
        return

    change_d['v'] = message.text
    await state.update_data(new_val=message.text)
    data = await state.get_data()
    await message.answer(f"Параметр: {chek_d.get(data['param'])[1]}\n\n"
                         f"Новое значение: {data['new_val']}")

    k = chek_d.get(data['param'])[0]
    v = data['new_val']
    change_stud_inform(message.from_user.id, k, v)

    await message.answer('Параметр изменен.', parse_mode='HTML', reply_markup=ikb_3)  # reply_markup=ikb_2
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
