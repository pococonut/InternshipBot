from aiogram import types

from create import dp
from commands.get_keyboard import get_account_keyboard
from commands.get_menu import callback_check_authentication
from commands.task_actions import check_user_values, get_check_page_title
from commands.general import read_user_values, write_user_values
from db.commands import select_added_users
from keyboard import added_ikb

account_values = read_user_values("account_values")


def get_account_info(account):
    """
    Функция просмотра информации добавленных аккаунтов.
    :param account: Строка модели БД, относящаяся к конкретному аккаунту, с информацией о нем.
    :return: Строка с информацией об аккаунте.
    """

    return f"<b>Пользователь:</b> {account.name_usr if account.name_usr else 'Отсутствует'}\n\n" \
           f"<b>Тип:</b> {account.type}\n\n" \
           f"<b>Логин:</b> {account.login}\n\n" \
           f"<b>Пароль:</b> {account.password}\n\n"


def get_accounts_message(callback, dict_name, dict_values):
    """
    Функция возвращает клавиатуру и информацию об аккаунте
    :param callback: Кнопка
    :param dict_name: Название словаря с навигацией пользователей
    :param dict_values: Словарь с навигацией пользователей
    :return: Клавиатура и информация об аккаунте
    """

    usr_id = str(callback.from_user.id)
    added_users = select_added_users()
    if not added_users:
        msg_text = 'Данные отсутствуют.\nЗагляните позже.'
        keyboard = get_account_keyboard(usr_id)
        return keyboard, msg_text

    dict_values = check_user_values(usr_id, dict_name, dict_values)
    result = get_check_page_title(callback, dict_name, dict_values, len(added_users))
    msg_text, dict_values = result
    write_user_values(dict_name, dict_values)

    current_account = added_users[dict_values[usr_id]]
    msg_text += get_account_info(current_account)
    return added_ikb, msg_text


@dp.callback_query_handler(text=["show_added_users", "left_added", "right_added"])
@callback_check_authentication
async def show_added(callback: types.CallbackQuery):
    """
    Функция просмотра добавленных аккаунтов.
    """

    keyboard, msg_text = get_accounts_message(callback, "account_values", account_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard)