from aiogram import types

from commands.get_menu import callback_check_authentication
from commands.task_actions import check_user_values, get_check_page_title
from create import dp
from commands.general import read_user_values, write_user_values, get_keyboard
from db.commands import select_added_users
from keyboard import added_ikb

globalDict_added = read_user_values("globalDict_added")


def show_inf_added(a):
    """
    Функция просмотра информации добавленных аккаунтов.
    :param a: Строка модели БД, относящаяся к конкретному аккаунту, с информацией о нем.
    :return: Строка с информацией об аккаунте.
    """

    return f"<b>Пользователь:</b> {a.name_usr if a.name_usr else 'Отсутствует'}\n\n" \
           f"<b>Тип:</b> {a.type}\n\n" \
           f"<b>Логин:</b> {a.login}\n\n" \
           f"<b>Пароль:</b> {a.password}\n\n"


def get_accounts_message(usr_id, callback, dict_name, dict_values):

    added_users = select_added_users()
    if not added_users:
        msg_text = 'Данные отсутствуют.\nЗагляните позже.'
        keyboard = get_keyboard(usr_id)
        return keyboard, msg_text

    dict_values = check_user_values(usr_id, dict_name, dict_values)
    result = get_check_page_title(usr_id, callback, dict_name, dict_values, len(added_users))
    msg_text, dict_values = result
    write_user_values(dict_name, dict_values)

    current_account = added_users[dict_values[usr_id]]
    msg_text += show_inf_added(current_account)
    return added_ikb, msg_text


@dp.callback_query_handler(text=["show_added_users", "left_added", "right_added"])
@callback_check_authentication
async def show_added(callback: types.CallbackQuery):
    """
    Функция просмотра добавленных аккаунтов.
    """

    usr_id = str(callback.from_user.id)
    keyboard, msg_text = get_accounts_message(usr_id, callback.data, "globalDict_added", globalDict_added)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard)