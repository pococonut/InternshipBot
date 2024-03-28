from aiogram import types
from aiogram.dispatcher import FSMContext
from commands.account_show import globalDict_added
from commands.get_menu import callback_check_authentication
from commands.task_actions import check_range
from create import dp
from commands.general import ConfirmDeletion
from db.commands import select_added_users, del_added
from keyboard import del_added_ikb, back_added_ikb


@dp.callback_query_handler(text='del_added')
@callback_check_authentication
async def del_a(callback: types.CallbackQuery):
    """
    Функция подтверждения удаления аккаунта.
    """

    await callback.message.edit_text('Удалить данные?', reply_markup=del_added_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_a_yes', state=ConfirmDeletion.delete)
@callback_check_authentication
async def del_a_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция удаления аккаунта.
    """

    await state.update_data(delete=callback.data)
    added = select_added_users()
    usr_id = str(callback.from_user.id)
    a_id = added[globalDict_added[usr_id]].id
    del_added(a_id)
    check_range(len(added), usr_id, "globalDict_added", globalDict_added)
    await state.finish()
    await callback.message.edit_text('Данные удалены.', reply_markup=back_added_ikb)