from db.commands import user_type, stud_approve
from keyboard import admin_ikb, worker_ikb, stud_is_approve, ikb_3
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

# -------------------- Отмена действия --------------------


async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    u_type = user_type(callback.from_user.id)

    if u_type is None:
        await callback.message.edit_text('Действие отменено.')
    else:
        keyboard = admin_ikb
        if u_type[0] == 'student':
            approve = stud_approve(callback.from_user.id)
            if approve:
                keyboard = stud_is_approve
            else:
                keyboard = ikb_3
        elif u_type[0] == 'worker':
            keyboard = worker_ikb

        await callback.message.edit_text('Действие отменено.', reply_markup=keyboard)


def register_handlers_back(dp: Dispatcher):
    dp.register_callback_query_handler(back_func, text='back', state="*")