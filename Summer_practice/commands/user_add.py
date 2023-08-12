from commands.back import back_func
from db.commands import add_user
from keyboard import admin_ikb, back_ikb, types_users, add_usr
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

# ------------------- Добавление сотрудников -------------------


class AddUser(StatesGroup):
    login = State()
    password = State()
    type = State()


types_w = {
           'admin': 'Администратор',
           'director': 'Директор',
           'worker': 'Сотрудник'
           }


async def add_user_command(callback: types.CallbackQuery):
    await callback.message.edit_text("Ведите новый <b>логин.</b>", parse_mode='HTML', reply_markup=back_ikb)
    await AddUser.login.set()


async def add_login(message: types.Message, state=FSMContext):
    await state.update_data(login=message.text)
    await message.answer('Ведите новый <b>пароль.</b>', parse_mode='HTML')
    await AddUser.next()


async def add_password(message: types.Message, state=FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Выберите <b>тип пользователя.</b>', parse_mode='HTML', reply_markup=types_users)
    await AddUser.next()


async def add_type(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(type=callback.data)
    data = await state.get_data()
    added_user = add_user(data)

    if added_user:
        await callback.message.edit_text(f'👨‍💼 <b>Добавлен пользователь</b>\n\n'
                             f'<b>Логин:</b> {data["login"]}\n\n'
                             f'<b>Пароль:</b> {data["password"]}\n\n'
                             f'<b>Тип пользователя:</b> {types_w.get(data["type"])}\n\n',
                             parse_mode='HTML', reply_markup=add_usr)
        await state.finish()
    else:
        await callback.message.edit_text(f'Введенный логин или пароль уже существует.', reply_markup=add_usr)
        await state.finish()


"""async def add_phone(message: types.Message, state=FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('Введите <b>ФИО.</b>', parse_mode='HTML', reply_markup=skip_n)
    await AddUser.next()


async def skip_phone(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(phone=None)
    await callback.message.edit_text('Введите <b>ФИО.</b>', parse_mode='HTML', reply_markup=skip_n)
    await AddUser.next()
    
    
async def get_name(message: types.Message, state=FSMContext):
    await state.update_data(name=" ".join([i.capitalize() for i in message.text.split()]))
    data = await state.get_data()
    added_user = add_user(data)
    if added_user:
        await message.answer(f'👨‍💼 <b>Добавлен пользователь</b>\n\n'
                             f'<b>Логин:</b> {data["login"]}\n\n'
                             f'<b>Пароль:</b> {data["password"]}\n\n'
                             f'<b>Тип пользователя:</b> {types_w.get(data["type"])}\n\n'
                             f'<b>Номер телефона:</b> {data["phone"] if data["phone"] is not None else "Нет"}\n\n'
                             f'<b>ФИО:</b> {data["name"] if data["name"] is not None else "Нет"}',
                             parse_mode='HTML', reply_markup=admin_ikb)
        await state.finish()
    else:
        print(added_user)


async def skip_name(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(name=None)
    data = await state.get_data()
    added_user = add_user(data)
    if added_user:
        await callback.message.answer(f'👨‍💼 <b>Добавлен пользователь</b>\n\n'
                             f'<b>Логин:</b> {data["login"]}\n\n'
                             f'<b>Пароль:</b> {data["password"]}\n\n'
                             f'<b>Тип пользователя:</b> {types_w.get(data["type"])}\n\n'
                             f'<b>Номер телефона:</b> {data["phone"] if data["phone"] is not None else "Нет"}\n\n'
                             f'<b>ФИО:</b> {data["name"] if data["name"] is not None else "Нет"}',
                             parse_mode='HTML', reply_markup=admin_ikb)
        await state.finish()"""


def register_handlers_add_user(dp: Dispatcher):
    dp.register_callback_query_handler(add_user_command, text='add_user')
    dp.register_message_handler(add_login, state=AddUser.login)
    dp.register_message_handler(add_password, state=AddUser.password)
    dp.register_callback_query_handler(add_type, text=['director', 'admin', 'worker'], state=AddUser.type)
    dp.register_callback_query_handler(back_func, text='back', state="*")