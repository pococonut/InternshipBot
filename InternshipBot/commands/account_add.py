from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import dp
from db.commands import add_user
from commands.get_menu import callback_check_authentication, message_check_authentication
from keyboard import back_ikb, types_users, admin_accounts_ikb


class Account(StatesGroup):
    login = State()
    password = State()
    type = State()


@dp.callback_query_handler(text='add_user')
@callback_check_authentication
async def add_user_command(callback: types.CallbackQuery):
    """
    Функция начала добавления аккаунта
    """

    await callback.message.edit_text("Ведите новый <b>логин.</b>", parse_mode='HTML', reply_markup=back_ikb)
    await Account.login.set()


@dp.message_handler(state=Account.login)
async def add_login(message: types.Message, state=FSMContext):
    """
    Функция получения параметра аккаунта - Пароль.
    """

    await state.update_data(login=message.text)
    await message.answer('Ведите новый <b>пароль.</b>', parse_mode='HTML')
    await Account.next()


@dp.message_handler(state=Account.password)
async def add_password(message: types.Message, state=FSMContext):
    """
    Функция получения параметра аккаунта - Логин.
    """

    await state.update_data(password=message.text)
    await message.answer('Выберите <b>тип пользователя.</b>', parse_mode='HTML', reply_markup=types_users)
    await Account.next()


@dp.callback_query_handler(text=['director', 'admin', 'worker'], state=Account.type)
async def add_type(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция получения параметра аккаунта - Тип пользователя (Директор, Администратор, Студент, Сотрудник).
    """

    types_w = {'admin': 'Администратор',
               'director': 'Директор',
               'worker': 'Сотрудник'}

    await state.update_data(type=callback.data)
    data = await state.get_data()
    added_user = add_user(data)

    if added_user:
        msg_text = f'👨‍💼 <b>Добавлен пользователь</b>\n\n' \
                   f'<b>Логин:</b> {data["login"]}\n\n' \
                   f'<b>Пароль:</b> {data["password"]}\n\n' \
                   f'<b>Тип пользователя:</b> {types_w.get(data["type"])}'
    else:
        msg_text = 'Введенный логин или пароль уже существует.'

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=admin_accounts_ikb)
    await state.finish()
