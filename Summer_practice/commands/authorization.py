from commands.back import back_func
from db.commands import user_type, register_admin, register_director, register_worker
from keyboard import admin_ikb, worker_ikb, back_ikb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import string


# ------------------- Регистрация сотрудников -------------------


class Authorisation(StatesGroup):
    login = State()
    password = State()
    name = State()


authorisation_lst = []

log_pass = {'admin': [['1', '111'], ['0', '000']],
            'director': [['2', '222'], ],
            'worker': [['3', '333'], ['4', '444']],}


def chek_wlogin(l, *args):
    f = False
    for i in args[0]:
        if i[0] == l:
            f = True
    return f


def chek_wpassword(p, *args):
    f = False
    for i in args[0]:
        if i[1] == p:
            f = True
    return f


async def authorization_command(message: types.Message):
    u_type = user_type(message.from_user.id)
    print(u_type)

    if u_type is None:
        await message.answer(f'Введите <b>логин.</b>', parse_mode='HTML', reply_markup=back_ikb)
        await Authorisation.login.set()
    elif u_type[0] in ('admin', 'director'):
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=admin_ikb)
    elif u_type[0] == 'worker':
        await message.answer("Выберите команду.", parse_mode='HTML', reply_markup=worker_ikb)
    elif u_type[0] == 'student':
        await message.answer("Вы не являетесь сотрудником.", parse_mode='HTML')


async def get_login(message: types.Message, state=FSMContext):
    m = message.text
    if not chek_wlogin(m, log_pass.get('admin')) and not chek_wlogin(m, log_pass.get('director')) \
            and not chek_wlogin(m, log_pass.get('worker')):
        await message.answer("Введен неверный логин.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(login=message.text)
    await message.answer('Введите <b>пароль.</b>', parse_mode='HTML')
    await Authorisation.next()


async def get_password(message: types.Message, state=FSMContext):
    m = message.text
    if not chek_wpassword(m, log_pass.get('admin')) and not chek_wpassword(m, log_pass.get(
            'director')) and not chek_wpassword(m, log_pass.get('worker')):
        await message.answer("Введен неверный пароль.\nПожалуйста, повторите ввод.")
        return
    await state.update_data(password=message.text)
    await message.answer("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>", parse_mode='HTML')
    await Authorisation.next()


async def get_name(message: types.Message, state=FSMContext):
    if len(message.text.split()) != 3 or any(chr.isdigit() for chr in message.text) or any(
            chr in string.punctuation for chr in message.text):
        await message.answer('ФИО введено в некорректом формате', parse_mode='HTML')
        return
    await state.update_data(name=" ".join([i.capitalize() for i in message.text.split()]))
    data = await state.get_data()
    if chek_wlogin(data.get('login'), log_pass.get('admin')) and \
            chek_wpassword(data.get('password'), log_pass.get('admin')):
        admin = register_admin(message.from_user.id, data)
        if admin:
            who = 'администатор'
            keyboard = admin_ikb
    elif chek_wlogin(data.get('login'), log_pass.get('director')) and \
            chek_wpassword(data.get('password'), log_pass.get('director')):
        director = register_director(message.from_user.id, data)
        if director:
            who = 'директор'
            keyboard = admin_ikb
    elif chek_wlogin(data.get('login'), log_pass.get('worker')) and \
            chek_wpassword(data.get('password'), log_pass.get('worker')):
        worker = register_worker(message.from_user.id, data)
        if worker:
            who = 'сотрудник'
            keyboard = worker_ikb
    await message.answer(f'Вы авторизированны как <b>{who}</b>.', parse_mode='HTML')
    await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=keyboard)

    await state.finish()


def register_handlers_authorization(dp: Dispatcher):
    dp.register_message_handler(authorization_command, commands=['menu'])
    dp.register_message_handler(get_login, state=Authorisation.login)
    dp.register_message_handler(get_password, state=Authorisation.password)
    dp.register_message_handler(get_name, state=Authorisation.name)
    dp.register_callback_query_handler(back_func, text='back', state="*")