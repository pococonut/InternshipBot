from create import dp
from aiogram import types
from db.commands import user_type
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard
from keyboard import add_usr, back_applications


lst_back = ['back', 'back_added', 'back_application']


@dp.callback_query_handler(text=lst_back, state="*")
async def back_func1(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    u_type = user_type(callback.from_user.id)

    if u_type is None:
        await callback.message.edit_text('Действие отменено.')
    else:
        if callback.data == 'back_added':
            keyboard = add_usr
        elif callback.data == 'back_application':
            keyboard = back_applications
        else:
            keyboard = get_keyboard(callback.from_user.id)
        await callback.message.edit_text('Действие отменено.', reply_markup=keyboard)
