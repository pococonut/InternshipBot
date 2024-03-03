from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from commands.general import ConfirmDeletion, navigation, read_user_values, write_user_values
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.commands import add_user, select_added_users, del_added
from keyboard import back_ikb, types_users, add_usr, added_ikb, del_added_ikb, back_added_ikb, login_added_ikb


globalDict_added = read_user_values("globalDict_added")

types_w = {
    'admin': 'Администратор',
    'director': 'Директор',
    'worker': 'Сотрудник'
}


class AddUser(StatesGroup):
    login = State()
    password = State()
    type = State()


def show_inf_added(a):
    """
    Функция просмотра информации добавленных аккаунтов.
    :param a: Строка модели БД, относящаяся к конкретному аккаунту, с информацией о нем.
    :return: Строка с информацией об аккаунте.
    """
    v = f"*Пользователь\\:* {a.name_usr if a.name_usr is not None else 'Отсутствует'}\n\n" \
        f"*Тип\\:* {a.type}\n\n" \
        f"*Логин\\:* ||{a.login}||\n\n" \
        f"*Пароль\\:* ||{a.password}||\n\n"
    return v


@dp.callback_query_handler(text='add_user')
async def add_user_command(callback: types.CallbackQuery):
    await callback.message.edit_text("Ведите новый <b>логин.</b>", parse_mode='HTML', reply_markup=back_ikb)
    await AddUser.login.set()


@dp.message_handler(state=AddUser.login)
async def add_login(message: types.Message, state=FSMContext):
    """
    Функция получения параметра аккаунта - Пароль.
    """
    await state.update_data(login=message.text)
    await message.answer('Ведите новый <b>пароль.</b>', parse_mode='HTML')
    await AddUser.next()


@dp.message_handler(state=AddUser.password)
async def add_password(message: types.Message, state=FSMContext):
    """
    Функция получения параметра аккаунта - Логин.
    """
    await state.update_data(password=message.text)
    await message.answer('Выберите <b>тип пользователя.</b>', parse_mode='HTML', reply_markup=types_users)
    await AddUser.next()


@dp.callback_query_handler(text=['director', 'admin', 'worker'], state=AddUser.type)
async def add_type(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция получения параметра аккаунта - Тип пользователя (Директор, Администратор, Студент, Сотрудник).
    """
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


@dp.callback_query_handler(text=["show_added_users", "left_added", "right_added"])
async def show_added(callback: types.CallbackQuery):
    """
    Функция просмотра добавленных аккаунтов.
    """
    added_users = select_added_users()
    if not added_users:
        # !!! дополнить
        await callback.message.edit_text('Данные отсутствуют.\nЗагляните позже.', reply_markup=add_usr)
        await callback.answer()
    else:
        usr_id = str(callback.from_user.id)
        count_added = len(added_users)

        if usr_id not in globalDict_added:
            globalDict_added[usr_id] = 0
            write_user_values("globalDict_added", globalDict_added)

        if callback.data == 'show_added_users':
            a = globalDict_added[usr_id]
            if globalDict_added[usr_id] <= -1:
                a = count_added + globalDict_added[usr_id]

            if added_users[a].name_usr is not None:
                keyboard = login_added_ikb
            else:
                keyboard = added_ikb

            await callback.message.edit_text(f"*№\\ *{a + 1}/{count_added}\n\n" + show_inf_added(added_users[a]),
                                             parse_mode='MarkdownV2',
                                             reply_markup=keyboard,
                                             disable_web_page_preview=True)
        else:
            s, globalDict_added[usr_id] = navigation(callback.data, globalDict_added[usr_id], count_added)
            write_user_values("globalDict_added", globalDict_added)
            if added_users[globalDict_added[usr_id]].name_usr is not None:
                keyboard = login_added_ikb
            else:
                keyboard = added_ikb
            await callback.message.edit_text(s + show_inf_added(added_users[globalDict_added[usr_id]]),
                                             parse_mode='MarkdownV2',
                                             reply_markup=keyboard,
                                             disable_web_page_preview=True)


@dp.callback_query_handler(text='del_added')
async def del_a(callback: types.CallbackQuery):
    """
    Функция подтверждения удаления аккаунта.
    """
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить данные?', parse_mode='HTML', reply_markup=del_added_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_a_yes', state=ConfirmDeletion.delete)
async def del_a_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция удаления аккаунта.
    """
    await state.update_data(delete=callback.data)
    added = select_added_users()
    usr_id = str(callback.from_user.id)
    a_id = added[globalDict_added[usr_id]].id
    del_added(a_id)
    count_added = len(added)

    if count_added is not None and (globalDict_added[usr_id] >= count_added or globalDict_added[usr_id] < count_added):
        globalDict_added[usr_id] = 0
        write_user_values("globalDict_added", globalDict_added)

    await state.finish()
    await callback.message.edit_text('Данные удалены', parse_mode='HTML', reply_markup=back_added_ikb)