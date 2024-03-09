from create import dp
from aiogram import types
from db.commands import user_type
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard
from keyboard import add_usr, back_applications, back_task_w_ikb

lst_back = ['back', 'back_added', 'back_application', 'back_tasks']


@dp.callback_query_handler(text=lst_back, state="*")
async def back_func1(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция для отмены действия.
    """

    user_id = callback.from_user.id
    u_type = user_type(user_id)
    await state.finish()
    await callback.message.edit_reply_markup()

    if not u_type:
        await callback.message.edit_text('Действие отменено.')
    else:
        if callback.data == 'back_added':
            keyboard = add_usr
        elif callback.data == 'back_application':
            keyboard = back_applications
        elif callback.data == 'back_tasks':
            keyboard = back_task_w_ikb
        else:
            keyboard = get_keyboard(user_id)
        await callback.message.edit_text('Действие отменено.', reply_markup=keyboard)
