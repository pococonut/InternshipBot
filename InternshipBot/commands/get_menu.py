import functools

from aiogram import types

from create import dp
from db.commands import get_user_type
from commands.get_keyboard import get_account_keyboard
from keyboard import new_user_ikb, chat_ikb, admin_tasks_ikb, admin_students_ikb, admin_accounts_ikb

unauthorized_msg = (f'Выберите команду.\n<em>Регистрация</em> -  Для студентов.'
                    f'\n<em>Авторизация</em> - Для сотрудников.')


def message_check_authentication(func):
    """
    Функция для проверки регистрации пользователя
    """

    @functools.wraps(func)
    async def wrapper(message: types.Message):
        user_id = message.from_user.id
        user_exist = get_user_type(user_id)
        if not user_exist:
            await message.answer(unauthorized_msg, parse_mode='HTML', reply_markup=new_user_ikb)
        else:
            await func(message)
    return wrapper


def callback_check_authentication(func):
    """
    Функция для проверки регистрации пользователя
    """

    @functools.wraps(func)
    async def wrapper(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        user_exist = get_user_type(user_id)
        if not user_exist:
            await callback.message.edit_text(unauthorized_msg, parse_mode='HTML', reply_markup=new_user_ikb)
        else:
            await func(callback)
    return wrapper


@dp.message_handler(commands=['menu'])
@message_check_authentication
async def menu_get(message: types.Message):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """

    user_id = message.from_user.id
    await message.answer('Выберите команду.', reply_markup=get_account_keyboard(user_id))


@dp.callback_query_handler(text='menu')
@callback_check_authentication
async def menu_get_inline(callback: types.CallbackQuery):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """

    user_id = callback.from_user.id
    await callback.message.edit_text('Выберите команду.', reply_markup=get_account_keyboard(user_id))


@dp.callback_query_handler(text="tasks_actions")
@callback_check_authentication
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю команд для задач.
    """

    msg_text = "Выберите команду."
    keyboard = admin_tasks_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text="students_actions")
@callback_check_authentication
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю команд для работы с заявками/студентами.
    """

    msg_text = "Выберите команду."
    keyboard = admin_students_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text="accounts_actions")
@callback_check_authentication
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю команд для работы с аккаунтами.
    """

    msg_text = "Выберите команду."
    keyboard = admin_accounts_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='chat')
@callback_check_authentication
async def chat_command(callback: types.CallbackQuery):
    """
    Функция возвращающая ссылку на общий чат.
    """

    msg_text = "Чат для связи доступен по ссылке - https://t.me/+FShhqiWUDJRjODky."
    await callback.message.edit_text(msg_text, disable_web_page_preview=True, reply_markup=chat_ikb)
