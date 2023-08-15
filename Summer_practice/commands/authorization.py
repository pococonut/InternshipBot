from commands.back import back_func
from db.commands import user_type, register_admin, register_director, register_worker, stud_approve, select_added_users, \
    change_name_added
from keyboard import admin_ikb, worker_ikb, back_ikb, stud_is_approve, ikb_3, chat_ikb, login_rep
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import phonenumbers
import string


# ------------------- Регистрация сотрудников -------------------


class Authorisation(StatesGroup):
    login = State()
    password = State()
    phone = State()
    name = State()


def check(l, p):
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


async def authorization_command_inline(callback: types.CallbackQuery):
    u_type = user_type(callback.from_user.id)
    print(u_type)

    if u_type is None:
        await callback.message.edit_text(f'Введите <b>логин.</b>', parse_mode='HTML', reply_markup=back_ikb)
        await Authorisation.login.set()
    elif u_type[0] in ('admin', 'director'):
        await callback.message.edit_text("Выберите команду.", parse_mode='HTML', reply_markup=admin_ikb)
    elif u_type[0] == 'worker':
        await callback.message.edit_text("Выберите команду.", parse_mode='HTML', reply_markup=worker_ikb)
    elif u_type[0] == 'student':
        approve = stud_approve(callback.from_user.id)
        keyboard = ikb_3
        if approve:
            keyboard = stud_is_approve
        await callback.message.edit_text("Выберите команду.", parse_mode='HTML', reply_markup=keyboard)


async def get_login(message: types.Message, state=FSMContext):
    await state.update_data(login=message.text)
    await message.answer('Введите <b>пароль.</b>', parse_mode='HTML')
    await Authorisation.next()


async def get_password(message: types.Message, state=FSMContext):
    data = await state.get_data()
    info = check(data['login'], message.text)
    if not info:
        await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
        await state.finish()
        return

    await state.update_data(password=message.text)
    await message.answer("Введите <b>Номер телефона, привязанный к telegram</b> в формате: <em>+79963833254</em>",
                             parse_mode='HTML')
    await Authorisation.next()


async def get_phone(message: types.Message, state=FSMContext):
    print('fffffffff')

    m = message.text
    try:
        phonenumbers.parse(m)
        await state.update_data(phone=m)
        await message.answer("Введите <b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>", parse_mode='HTML')
    except:
        await message.answer("Введен неверный формат.\nПожалуйста, повторите ввод.")
        return

    await Authorisation.next()


async def get_name(message: types.Message, state=FSMContext):
    print('nnnnnnnn')

    data = await state.get_data()
    info = check(data['login'], data['password'])
    m = message.text
    if len(m.split()) != 3 or any(chr.isdigit() for chr in m) or any(chr in string.punctuation for chr in m):
        await message.answer('ФИО введено в некорректном формате', parse_mode='HTML')
        return
    await state.update_data(name=" ".join([i.capitalize() for i in m.split()]))
    data = await state.get_data()

    who = False
    if info['type'] == 'admin':
        print('admin')
        admin = register_admin(message.from_user.id, data)
        if admin:
            who = 'администратор'
            keyboard = admin_ikb
        else:
            await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
    elif info['type'] == 'director':
        director = register_director(message.from_user.id, data)
        if director:
            who = 'директор'
            keyboard = admin_ikb
        else:
            await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)
    elif info['type'] == 'worker':
        worker = register_worker(message.from_user.id, data)
        if worker:
            who = 'сотрудник'
            keyboard = worker_ikb
        else:
            await message.answer("Введен неверный логин или пароль.", reply_markup=login_rep)

    if who:
        print(data.get('login'), data.get('name'))
        change_name_added(data.get('login'), data.get('name'))
        await message.answer(f'Вы авторизированны как <b>{who}</b>.\n\nЧат для связи доступен по ссылке - https://t.me/+FShhqiWUDJRjODky',
                             disable_web_page_preview=True, parse_mode='HTML')
        await message.answer('Выберите команду.', parse_mode='HTML', reply_markup=keyboard)

    await state.finish()


async def chat_command(callback: types.CallbackQuery):
    await callback.message.edit_text("Чат для связи доступен по ссылке - https://t.me/+FShhqiWUDJRjODky.",
                                      disable_web_page_preview=True, reply_markup=chat_ikb)


def register_handlers_authorization(dp: Dispatcher):
    dp.register_message_handler(authorization_command, commands=['menu'])
    dp.register_callback_query_handler(authorization_command_inline, text='menu')
    dp.register_callback_query_handler(chat_command, text='chat')
    dp.register_message_handler(get_login, state=Authorisation.login)
    dp.register_message_handler(get_password, state=Authorisation.password)
    dp.register_message_handler(get_phone, state=Authorisation.phone)
    dp.register_message_handler(get_name, state=Authorisation.name)
    dp.register_callback_query_handler(back_func, text='back', state="*")