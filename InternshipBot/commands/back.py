from create import dp
from aiogram import types
from db.commands import get_user_type
from aiogram.dispatcher import FSMContext
from commands.get_keyboard import get_account_keyboard
from commands.task_change import values_user_type
from keyboard import back_applications, back_task_w_ikb, back_task_own_ikb, admin_accounts_ikb

back_keyboards = {'back_added': admin_accounts_ikb,
                  'back_application': back_applications,
                  'back_tasks': back_task_w_ikb,
                  'back_change_tasks': [back_task_own_ikb, back_task_w_ikb],
                  'back': None}

lst_back = list(back_keyboards.keys())


def get_back_keyboard(user_id, callback):
    """
    Функция возвращает клавиатуру в зависимости от действия, которое было отменено
    :param user_id: Идентификатор пользователя в телеграм
    :param callback: Кнопка
    :return: Клавиатура
    """

    if callback == 'back_change_tasks':
        keyboards = back_keyboards.get(callback)
        if values_user_type and 'worker' in values_user_type.get(user_id):
            del values_user_type[user_id]
            return keyboards[0]
        return keyboards[1]

    keyboard = back_keyboards.get(callback)
    if not keyboard:
        return get_account_keyboard(user_id)
    return keyboard


@dp.callback_query_handler(text=lst_back, state="*")
async def back(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция для отмены действия.
    """

    await state.finish()
    user_id = str(callback.from_user.id)
    user_type = get_user_type(user_id)
    msg_text = 'Действие отменено.'
    keyboard = get_back_keyboard(user_id, callback.data)

    if not user_type:
        await callback.message.edit_text(msg_text)
        return

    await callback.message.edit_text(msg_text, reply_markup=keyboard)
