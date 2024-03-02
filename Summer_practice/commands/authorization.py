import string
import phonenumbers
from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard
from keyboard import admin_ikb, worker_ikb, login_rep
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.commands import select_added_users, change_name_added, registration_user


class Authorisation(StatesGroup):
    login = State()
    password = State()
    phone = State()
    name = State()


def check(l, p):
    """
    Функция проверки логина и пароля на соответствие.

    :param l: Введенный пользователем Логин.
    :param p: Введенный пользователем Пароль.
    :return: Флаг, (f = False - логин или пароль неверный, f = словарь хранящий логин, пароль и тип пользователя).
    """
    authorisation_lst = {}

    for u in select_added_users():
        inf = {'type': u.type,
               'login': u.login,
               'password': u.password,
               }
        authorisation_lst[u.id] = inf

    f = False
    for key, inf in authorisation_lst.items():
        if inf.get('login') == l and inf.get('password') == p:
            f = inf
    return f


@dp.callback_query_handler(text='authorization')
async def authorization_command(callback: types.CallbackQuery):
    """
    Функция начала процесса авторизации.
    """
    keyboard = get_keyboard(callback.from_user.id)
    await callback.message.edit_text(f'Введите <b>логин.</b>', parse_mode='HTML', reply_markup=keyboard)
    await Authorisation.login.set()


@dp.message_handler(state=Authorisation.login)
async def get_login(message: types.Message, state=FSMContext):
    """
    Функция получения логина от пользователя.
    """
    await state.update_data(login=message.text)
    await message.answer('Введите <b>пароль.</b>', parse_mode='HTML')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.password)
async def get_password(message: types.Message, state=FSMContext):
    """
    Функция получения пароля от пользователя.
    """
    data = await state.get_data()
    info = check(data['login'], message.text)
    if not info:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
        await state.finish()
        return

    await state.update_data(password=message.text)
    await message.answer("Введите <b>Номер телефона, привязанный к telegram</b> в формате: <code><em>+79999999999</em></code>",
                         parse_mode='HTML')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.phone)
async def get_phone(message: types.Message, state=FSMContext):
    """
    Функция получения номера телефона от пользователя.
    """
    m = message.text
    try:
        phonenumbers.parse(m)
        await state.update_data(phone=m)
        await message.answer("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>", parse_mode='HTML')
    except:
        await message.answer("Введен неверный формат.\nПожалуйста, повторите ввод.")
        return
    await Authorisation.next()


@dp.message_handler(state=Authorisation.name)
async def get_name(message: types.Message, state=FSMContext):
    """
    Функция получения ФИО от пользователя.
    """
    data = await state.get_data()
    info = check(data['login'], data['password'])
    m = message.text
    if len(m.split()) != 3 or any(chr.isdigit() for chr in m) or any(chr in string.punctuation for chr in m):
        await message.answer('ФИО введено в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(name=" ".join([i.capitalize() for i in m.split()]))
    data = await state.get_data()

    who = registration_user(message.from_user.id, info['type'], data)

    if not who:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
    else:
        keyboard = admin_ikb
        if who == 'сотрудник':
            keyboard = worker_ikb

        change_name_added(data.get('login'), data.get('name'))
        await message.answer(f'Вы авторизованны как <b>{who}</b>.\n\nЧат для связи доступен по ссылке - '
                             f'https://t.me/+FShhqiWUDJRjODky', disable_web_page_preview=True, parse_mode='HTML')
        await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=keyboard)

    await state.finish()

