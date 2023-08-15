from commands.back import back_func
from db.commands import add_user, select_added_users, del_added
from keyboard import admin_ikb, back_ikb, types_users, add_usr, added_ikb, del_added_ikb, back_added_ikb, \
    login_added_ikb
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
        await callback.message.edit_text(f'👨‍💼 *Добавлен пользователь\\ *\n\n'
                             f'*Логин\\:* ||{data["login"]}||\n\n'
                             f'*Пароль\\:* ||{data["password"]}||\n\n'
                             f'*Тип пользователя\\:* {types_w.get(data["type"])}\n\n',
                             parse_mode='MarkdownV2', reply_markup=add_usr)
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

        if added_users[a].name_usr is not None:
            keyboard = login_added_ikb
        else:
            keyboard = added_ikb

        await callback.message.edit_text(
            f"*№\\ *{a + 1}/{count_added}\n\n"
            f"*Пользователь\\:* {added_users[a].name_usr if added_users[a].name_usr is not None else 'Отсутствует'}\n\n"
            f"*Тип\\:* {added_users[a].type}\n\n"
            f"*Логин\\:* ||{added_users[a].login}||\n\n"
            f"*Пароль\\:* ||{added_users[a].password}||\n\n",
            parse_mode='MarkdownV2',
            reply_markup=keyboard,
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
            s = f"*№\\ *{a_r + 1}/{count_added}\n\n"

        if callback.data == 'left_added':
            globalDict_added[usr_id] -= 1
            a_l = 0
            if globalDict_added[usr_id] == (-1) * count_added:
                globalDict_added[usr_id] = 0
            if globalDict_added[usr_id] <= -1:
                a_l = count_added
            s = f"*№\\ *{(a_l + globalDict_added[usr_id]) + 1}/{count_added}\n\n"
        print(globalDict_added)

        if added_users[globalDict_added[usr_id]].name_usr is not None:
            keyboard = login_added_ikb
        else:
            keyboard = added_ikb
        await callback.message.edit_text(s + f"*Пользователь\\:* {added_users[globalDict_added[usr_id]].name_usr if added_users[globalDict_added[usr_id]].name_usr is not None else 'Отсутствует'}\n\n"
                                             f"*Тип\\:* {added_users[globalDict_added[usr_id]].type}\n\n"
                                             f"*Логин\\:* ||{added_users[globalDict_added[usr_id]].login}||\n\n"
                                             f"*Пароль\\:* ||{added_users[globalDict_added[usr_id]].password}||\n\n",
                                             parse_mode='MarkdownV2',
                                             reply_markup=keyboard,
                                             disable_web_page_preview=True)


class AddedDel(StatesGroup):
    del_a = State()


async def del_a(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    usr_id = str(callback.from_user.id)
    print("delete ", globalDict_added[usr_id] + 1)
    await callback.message.answer('Удалить данные?', parse_mode='HTML', reply_markup=del_added_ikb)
    await AddedDel.del_a.set()


async def del_a_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(del_a=callback.data)
    added = select_added_users()
    usr_id = str(callback.from_user.id)
    a_id = added[globalDict_added[usr_id]].id
    del_added(a_id)
    await state.finish()
    await callback.message.edit_text('Данные удалены', parse_mode='HTML', reply_markup=back_added_ikb)


def register_handlers_add_user(dp: Dispatcher):
    dp.register_callback_query_handler(add_user_command, text='add_user')
    dp.register_message_handler(add_login, state=AddUser.login)
    dp.register_message_handler(add_password, state=AddUser.password)
    dp.register_callback_query_handler(add_type, text=['director', 'admin', 'worker'], state=AddUser.type)
    dp.register_callback_query_handler(show_added, text='show_add_user')
    dp.register_callback_query_handler(show_added_rl, text=["left_added", "right_added"])
    dp.register_callback_query_handler(del_a, text='del_added')
    dp.register_callback_query_handler(del_a_yes, text='del_a_yes', state=AddedDel.del_a)
    dp.register_callback_query_handler(back_func, text='back', state="*")