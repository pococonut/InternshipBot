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


def check_user_name(name):
    """
    Функция для валидации ФИО
    Args:
        name: ФИО пользователя

    Returns: True - ФИО корректно, False - ФИО некорректно
    """

    if len(name) > 60:
        return False

    if len(name.split()) != 3:
        return False

    no_numbers = name.replace(" ", "").replace("-", "").isalpha()
    if not no_numbers:
        return False

    return True


def make_name_capital_letters(user_name):
    """
    Функция для привидения первых букв в ФИО к верхнему регистру
    Args:
        user_name: ФИО пользователя

    Returns: ФИО в правильном формате
    """

    return " ".join([w.capitalize() for w in user_name.split()])


def check_login(login, password):
    """
    Функция проверки логина и пароля на соответствие.

    :param login: Введенный пользователем Логин.
    :param password: Введенный пользователем Пароль.
    :return: Флаг, (f = False - логин или пароль неверный, f = словарь хранящий логин, пароль и тип пользователя).
    """
    authorisation_lst = {}

    for u in select_added_users():
        inf = {'type': u.type, 'login': u.login, 'password': u.password}
        authorisation_lst[u.id] = inf

    f = False
    for key, inf in authorisation_lst.items():
        if inf.get('login') == login and inf.get('password') == password:
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
    info = check_login(data['login'], message.text)
    if not info:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
        await state.finish()
        return

    await state.update_data(password=message.text)
    msg_text = ("Введите <b>Номер телефона, привязанный к telegram</b> "
                "в формате: <code><em>+79999999999</em></code>")
    await message.answer(msg_text, parse_mode='HTML')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.phone)
async def get_phone(message: types.Message, state=FSMContext):
    """
    Функция получения номера телефона от пользователя.
    """
    try:
        phone = message.text
        phonenumbers.parse(phone)
        await state.update_data(phone=phone)
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
    info = check_login(data['login'], data['password'])
    name = message.text
    if not check_user_name(name):
        await message.answer('ФИО введено в некорректном формате', parse_mode='HTML')
        return

    await state.update_data(name=make_name_capital_letters(name))
    data = await state.get_data()
    who = registration_user(message.from_user.id, info['type'], data)

    if not who:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
    else:
        keyboard = admin_ikb
        if who == 'сотрудник':
            keyboard = worker_ikb

        change_name_added(data.get('login'), data.get('name'))

        msg_text = (f'Вы авторизованны как <b>{who}</b>.\n\n'
                    'Чат для связи доступен по <a href="https://t.me/+FShhqiWUDJRjODky">этой ссылке</a>')

        await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
    await state.finish()

