from create import dp
from aiogram import types
from db.commands import get_user_type
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard
from keyboard import add_usr, back_applications, back_task_w_ikb

back_keyboards = {'back_added': add_usr,
                  'back_application': back_applications,
                  'back_tasks': back_task_w_ikb,
                  'back': None}

lst_back = list(back_keyboards.keys())


@dp.callback_query_handler(text=lst_back, state="*")
async def back_func1(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция для отмены действия.
    """

    await state.finish()
    await callback.message.edit_reply_markup()
    user_id = callback.from_user.id
    user_type = get_user_type(user_id)
    msg_text = 'Действие отменено.'

    if not user_type:
        await callback.message.edit_text(msg_text)
        return

    keyboard = back_keyboards.get(callback.data)
    if not keyboard:
        keyboard = get_keyboard(user_id)

    await callback.message.edit_text(msg_text, reply_markup=keyboard)
