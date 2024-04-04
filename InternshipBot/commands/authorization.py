import phonenumbers
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import dp
from commands.general import check_user_name, check_phone
from db.commands import select_added_users, registration_user
from keyboard import admin_ikb, worker_ikb, login_rep, back_ikb


class Authorisation(StatesGroup):
    login = State()
    password = State()
    phone = State()
    name = State()


def check_login(login, password):
    """
    Функция проверки логина и пароля на соответствие.

    :param login: Введенный пользователем Логин.
    :param password: Введенный пользователем Пароль.
    :return: Флаг, (f = False - логин или пароль неверный, f = словарь хранящий логин, пароль и тип пользователя).
    """

    authorisation_lst = {}

    for user in select_added_users():
        inf = {'type': user.type, 'login': user.login, 'password': user.password}
        authorisation_lst[user.id] = inf

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

    await callback.message.edit_text(f'Введите <b>логин.</b>', parse_mode='HTML', reply_markup=back_ikb)
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
    login = data['login']
    password = message.text
    result_of_check = check_login(login, password)
    if not result_of_check:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
        await state.finish()
        return

    msg_text = ("Введите <b>Номер телефона, привязанный к telegram</b> "
                "в формате: <code><em>+79999999999</em></code>")
    await state.update_data(password=password)
    await message.answer(msg_text, parse_mode='HTML')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.phone)
async def get_phone(message: types.Message, state=FSMContext):
    """
    Функция получения номера телефона от пользователя.
    """

    if not check_phone(message.text):
        await message.answer("Введен неверный формат.\nПожалуйста, повторите ввод.")
        return

    await state.update_data(phone=message.text)
    msg_text = "Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>"
    await message.answer(msg_text, parse_mode='HTML')
    await Authorisation.next()


@dp.message_handler(state=Authorisation.name)
async def get_name(message: types.Message, state=FSMContext):
    """
    Функция получения ФИО от пользователя.
    """

    name = check_user_name(message.text)
    if not name:
        msg_text = 'ФИО введено в некорректном формате'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(name=name)
    data = await state.get_data()

    user_type = registration_user(message.from_user.id, 'worker', data)
    if not user_type:
        msg_text = 'Ошибка авторизации.'
        await message.answer(msg_text, reply_markup=login_rep)
        return

    keyboard = admin_ikb
    if user_type == 'сотрудник':
        keyboard = worker_ikb

    msg_text = (f'Вы авторизованны как <b>{user_type}</b>.\n\n'
                'Чат для связи доступен по <a href="https://t.me/+FShhqiWUDJRjODky">этой ссылке</a>')
    await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
    await state.finish()

