from create import dp
from aiogram import types
from db.commands import select_user
from keyboard import change_user_ikb
from commands.general import print_stud


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


def show_inf(t_id):
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
async def show_params(message: types.Message):
    """
    Функция печати данных пользователя.
    """

    inf = show_inf(message.from_user.id)
    if not inf:
        msg_text = 'Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.'
        await message.answer(msg_text)
        return

    msg_text = f"🧑‍💻<b>Ваши данные</b>\n\n" + inf
    await message.answer(msg_text, parse_mode='HTML', reply_markup=change_user_ikb)


@dp.callback_query_handler(text='show')
async def show_params_inline(callback: types.CallbackQuery):
    """
    Функция печати данных пользователя.
    """

    inf = show_inf(callback.from_user.id)
    if not inf:
        msg_text = 'Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.'
        await callback.message.edit_text(msg_text)
        return

    msg_text = f"🧑‍💻<b>Ваши данные</b>\n\n" + inf
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=change_user_ikb)