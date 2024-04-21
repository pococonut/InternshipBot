from aiogram import types

from create import dp
from db.commands import select_user
from commands.general import print_stud
from commands.get_menu import callback_check_authentication, message_check_authentication
from keyboard import change_user_ikb


def print_worker(w):
    """
    Функция возвращающая данные сотрудника в виде строки.
    :param w: Строка модели БД, относящаяся к конкретному сотруднику, с информацией о нем.
    :return: Строка с данными сотрудника.
    """

    worker = f"<b>ФИО:</b> {w.name}\n\n" \
             f"<b>Номер телефона:</b> {w.phone}\n\n" \
             f"<b>Дата регистрации:</b> {w.reg_date}\n"
    return worker


def show_user_info(t_id):
    """
    Функция возвращающая информацию о пользователе в зависимости от его типа.
    :param t_id: Уникальный идентификатор пользователя в telegram
    :return: Данные пользователя.
    """

    user_show = select_user(t_id)
    if user_show is not None:
        if user_show.type == 'student':
            return print_stud(user_show)
        else:
            return print_worker(user_show)


@dp.message_handler(commands=['show'])
@message_check_authentication
async def show_params(message: types.Message):
    """
    Функция печати данных пользователя.
    """

    msg_text = f"🧑‍💻<b>Ваши данные</b>\n\n" + show_user_info(message.from_user.id)
    await message.answer(msg_text, parse_mode='HTML', reply_markup=change_user_ikb)


@dp.callback_query_handler(text='show')
@callback_check_authentication
async def show_params_inline(callback: types.CallbackQuery):
    """
    Функция печати данных пользователя.
    """

    msg_text = f"🧑‍💻<b>Ваши данные</b>\n\n" + show_user_info(callback.from_user.id)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=change_user_ikb)