from commands.back import back_func
from db.commands import add_user, select_added_users
from keyboard import admin_ikb, back_ikb, types_users, add_usr, added_ikb
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


globalDict_added = dict()


async def show_added(callback: types.CallbackQuery):
    added_users = select_added_users()
    if not added_users:
        # !!! дополнить
        await callback.message.edit_text('Данные отсутствуют.\nЗагляните позже.', reply_markup=add_usr)
    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_added:
            globalDict_added[usr_id] = 0
        print(globalDict_added)

        a = globalDict_added[usr_id]
        count_added = len(added_users)
        if globalDict_added[usr_id] <= -1:
            a = count_added + globalDict_added[usr_id]
        count_added = len(added_users)
        await callback.message.edit_text(
            f"<b>№</b> {a + 1}/{count_added}\n\n "
            f"Тип: {added_users[a].type}\n\n"
            f"Логин: {added_users[a].login}\n\n"
            f"Пароль: {added_users[a].password}\n\n",
            parse_mode='HTML',
            reply_markup=added_ikb,
            disable_web_page_preview=True)


async def show_added_rl(callback: types.CallbackQuery):
    added_users = select_added_users()
    if not added_users:
        # !!! дополнить
        await callback.message.edit_text('Данные отсутствуют.\nЗагляните позже.', reply_markup=add_usr)

    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_added:
            globalDict_added[usr_id] = 0

        count_added = len(added_users)
        s = ''
        if callback.data == 'right_added':
            globalDict_added[usr_id] += 1
            if globalDict_added[usr_id] == count_added:
                globalDict_added[usr_id] = 0
            a_r = globalDict_added[usr_id]
            if globalDict_added[usr_id] <= -1:
                a_r = count_added + globalDict_added[usr_id]
            s = f"<b>№</b> {a_r + 1}/{count_added}\n\n"

        if callback.data == 'left_added':
            globalDict_added[usr_id] -= 1
            a_l = 0
            if globalDict_added[usr_id] == (-1) * count_added:
                globalDict_added[usr_id] = 0
            if globalDict_added[usr_id] <= -1:
                a_l = count_added
            s = f"<b>№</b> {(a_l + globalDict_added[usr_id]) + 1}/{count_added}\n\n"
        print(globalDict_added)

        await callback.message.edit_text(s + f"Тип: {added_users[globalDict_added[usr_id]].type}\n\n"
                                             f"Логин: {added_users[globalDict_added[usr_id]].login}\n\n"
                                             f"Пароль: {added_users[globalDict_added[usr_id]].password}\n\n",
                                             parse_mode='HTML',
                                             reply_markup=added_ikb,
                                             disable_web_page_preview=True)


def register_handlers_add_user(dp: Dispatcher):
    dp.register_callback_query_handler(add_user_command, text='add_user')
    dp.register_message_handler(add_login, state=AddUser.login)
    dp.register_message_handler(add_password, state=AddUser.password)
    dp.register_callback_query_handler(add_type, text=['director', 'admin', 'worker'], state=AddUser.type)
    dp.register_callback_query_handler(show_added, text='show_add_user')
    dp.register_callback_query_handler(show_added_rl, text=["left_added", "right_added"])

    dp.register_callback_query_handler(back_func, text='back', state="*")