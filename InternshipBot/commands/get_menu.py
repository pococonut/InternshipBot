from create import dp
from aiogram import types
from db.commands import get_user_type
from commands.general import get_keyboard
from keyboard import new_user_ikb, chat_ikb, admin_tasks_ikb, admin_students_ikb, admin_accounts_ikb


def check_get_menu(user_id):
    """
    Функция для проверки регистрации пользователя
    :param user_id: Идентификатор пользователя в телеграм
    :return: Текст сообщения, клавиатура
    """

    user_exist = get_user_type(user_id)
    if not user_exist:
        msg_text = (f'Выберите команду.\n<em>Регистрация</em> -  Для студентов.'
                    f'\n<em>Авторизация</em> - Для сотрудников.')
        return msg_text, new_user_ikb
    return 'Выберите команду.', get_keyboard(user_id)


@dp.message_handler(commands=['menu'])
async def menu_get(message: types.Message):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """

    msg_text, keyboard = check_get_menu(message.from_user.id)
    await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard)


@dp.callback_query_handler(text='menu')
async def menu_get_inline(callback: types.CallbackQuery):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """

    msg_text, keyboard = check_get_menu(callback.from_user.id)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard)


@dp.callback_query_handler(text="tasks_actions")
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    msg_text = "Выберите команду."
    keyboard = admin_tasks_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text="students_actions")
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    msg_text = "Выберите команду."
    keyboard = admin_students_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text="accounts_actions")
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    msg_text = "Выберите команду."
    keyboard = admin_accounts_ikb
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='chat')
async def chat_command(callback: types.CallbackQuery):
    """
    Функция возвращающая ссылку на общий чат.
    """

    msg_text = "Чат для связи доступен по ссылке - https://t.me/+FShhqiWUDJRjODky."
    await callback.message.edit_text(msg_text, disable_web_page_preview=True, reply_markup=chat_ikb)