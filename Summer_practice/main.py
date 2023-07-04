from aiogram import Bot, Dispatcher, executor, types
from keyboard import ikb, kb, ikb_2, ikb_3, change_ikb, change_ikb_2
import string
from commands import register_student, select_student, change_stud_inform, get_txt, select_txt, delete_txt
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

TOKEN_API = ""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())  # инициализация входящих данных

HELP_COMMAND = """
<b>/help</b> - список комманд
<b>/description</b> - описание бота
<b>/registration</b> - регистрация студента
<b>/authorisation</b> - авторизация персонала
<b>/change</b> - изменение данных студента
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
    # await message.delete()  # удаляем сообщение пользователя, которое он отправил


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
    student_exist = select_student(message.from_user.id)
    if student_exist:
        await message.answer('Вы уже зарегестрированы', parse_mode='HTML', reply_markup=ikb_3)
        await message.edit_reply_markup()
        await message.delete()
    else:
        await message.answer(FORM, parse_mode='HTML')
        await message.answer("Введите ФИО")
    await Student.student_name.set()


@dp.message_handler(state=Student.student_name)
async def get_student_name(message: types.Message, state: FSMContext):
    student_exist = select_student(message.from_user.id)
    if student_exist:
        await state.finish()
        await state.reset_state(with_data=False)
    else:
        if len(message.text.split()) != 3 or any(chr.isdigit() for chr in message.text) or any(
                chr in string.punctuation for chr in message.text):
            await message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
            return
        await state.update_data(student_name=message.text)
        await message.answer("Введите ВУЗ")
        await Student.next()


@dp.message_handler(state=Student.university)
async def get_university(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 1 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(university=message.text)
    await message.answer("Введите Факультет")
    await Student.next()


@dp.message_handler(state=Student.faculty)
async def get_faculty(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Факультет введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(faculty=message.text)
    await message.answer("Введите Специальность")
    await Student.next()


@dp.message_handler(state=Student.specialties)
async def get_specialties(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Направление введено в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(specialties=message.text)
    await message.answer("Введите Кафедру")
    await Student.next()


@dp.message_handler(state=Student.department)
async def get_department(message: types.Message, state=FSMContext):
    if any(chr.isdigit() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Кафедра введена в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(department=message.text)
    await message.answer("Введите Курс")
    await Student.next()


@dp.message_handler(state=Student.course)
async def get_course(message: types.Message, state=FSMContext):
    if any(chr.isalpha() for chr in message.text) or any(chr in string.punctuation for chr in message.text):
        await message.answer('Курс введен в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(course=message.text)
    await message.answer("Введите Группу")
    await Student.next()


@dp.message_handler(state=Student.group)
async def get_group(message: types.Message, state=FSMContext):
    if any(chr.isalpha() for chr in message.text) or any(
            chr in string.punctuation.replace('./', '') for chr in message.text):
        await message.answer('Группа введена в неккоректом формате', parse_mode='HTML')
        return
    await state.update_data(group=message.text)
    await message.answer("Введите Курсовые")
    await Student.next()


@dp.message_handler(state=Student.coursework)
async def get_coursework(message: types.Message, state=FSMContext):
    await state.update_data(coursework=message.text)
    await message.answer("Введите Знания")
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


@dp.callback_query_handler(text='show')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    student_show = select_student(s_id)
    if student_show:

        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {student_show.student_name}\n\n"
                                      f"ВУЗ: {student_show.university}\n\n"
                                      f"Факультет: {student_show.faculty}\n\n"
                                      f"Специальность: {student_show.specialties}\n\n"
                                      f"Кафедра: {student_show.department}\n\n"
                                      f"Курс: {student_show.course}\n\n"
                                      f"Группа: {student_show.group}\n\n"
                                      f"Курсовые: {student_show.coursework}\n\n"
                                      f"Знания: {student_show.knowledge}\n\n"
                                      f"Дата регистрации: {student_show.reg_date}\n\n"
                                      )
    else:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')


class Change_student(StatesGroup):
    param = State()
    new_val = State()


ch_d = {'1': 'student_name',
        '2': 'university',
        '3': 'faculty',
        '4': 'specialties',
        '5': 'department',
        '6': 'course',
        '7': 'group',
        '8': 'coursework',
        '9': 'knowledge',
        }
@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    await message.answer(f'Введите номер параметра, который желаете изменить:\n\n'
                         f'ФИО - 1\n\n'
                         f'ВУЗ - 2\n\n'
                         f'Факультет - 3\n\n'
                         f'Направление - 4\n\n'
                         f'Кафедра - 5\n\n'
                         f'Курс - 6\n\n'
                         f'Группа - 7\n\n'
                         f'Темы курсовых работ - 8\n\n'
                         f'Ваши знания - 9\n\n'
                         )

    print(message.text)
    await Change_student.param.set()

@dp.message_handler(state=Change_student.param)
async def get_param(message: types.Message, state=FSMContext):
    await state.update_data(param=message.text)
    await message.answer("Введите новое значение")
    await Change_student.next()

@dp.message_handler(state=Change_student.new_val)
async def get_val(message: types.Message, state: FSMContext):

    await state.update_data(new_val=message.text)

    data = await state.get_data()
    await message.answer(f"Новые данные данные:\n\n"
                         f"Параметр: {data['param']}\n\n"
                         f"Новое значение: {data['new_val']}")

    k = ch_d.get(data['param'])
    v = data['new_val']
    change_stud_inform(message.from_user.id, k, v)
    #student = register_student(message.from_user.id, data)
    #if student:
    await message.answer('Параметр изменен.', parse_mode='HTML')  # , reply_markup=ikb_2
    await state.finish()
"""@dp.message_handler()
async def txt1(message: types.Message):
    get_txt(message.text)
    print("get text", message.text)"""


@dp.callback_query_handler(text='student_name')
async def f_callback(callback: types.CallbackQuery):
    print('!!!!!!!! ', callback.data)
    s_id = int(callback.from_user.id)

    # print('FUUUUUUCKKK')
    # if callback.data == 'student_name':

    if select_student(s_id) is None:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
    else:
        await callback.message.answer('Введите данные', parse_mode='HTML')

        if callback.data == 'student_name':
            print('s_name: ', callback.data)

            print('Параметр: ', callback.data)

            if select_txt() != []:
                txt = select_txt()[0][0]
                print(txt)

                if (len(txt.split()) != 3 or any(chr.isdigit() for chr in txt) or any(
                        chr in string.punctuation for chr in txt)):
                    await callback.message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, " ".join(i.capitalize() for i in txt.split(' ')))
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                    print("delete")
                    delete_txt()


@dp.callback_query_handler(text='university')
async def f_callback(callback: types.CallbackQuery):
    print('!!!!!!!! ', callback.data)
    s_id = int(callback.from_user.id)

    # print('FUUUUUUCKKK')
    # if callback.data == 'student_name':

    if select_student(s_id) is None:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
    else:
        await callback.message.answer('Введите данные', parse_mode='HTML')

        if callback.data == 'university':
            print('university: ', callback.data)

            print('Параметр: ', callback.data)

            if select_txt() != []:

                university = select_txt()[0][0]

                if (len(university.split()) != 1 or any(chr.isdigit() for chr in university) or any(
                        chr in string.punctuation for chr in university)):
                    await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, university.upper())
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                    print(university)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
