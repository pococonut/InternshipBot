from create import dp
from aiogram import types
from db.commands import user_type
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard


@dp.callback_query_handler(text='back', state="*")
async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    u_type = user_type(callback.from_user.id)

    if u_type is None:
        await callback.message.edit_text('Действие отменено.')
    else:
        keyboard = get_keyboard(callback.from_user.id)
        await callback.message.edit_text('Действие отменено.', reply_markup=keyboard)