from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import dp
from db.commands import del_all_data
from commands.get_keyboard import get_account_keyboard
from commands.get_menu import callback_check_authentication
from keyboard import clear_ikb, clear_confirm_ikb

clear_list = ['clr_accounts', 'clr_users', 'clr_workers', 'clr_students', 'clr_tasks']


class Clear(StatesGroup):
    command = State()
    delete = State()


@dp.callback_query_handler(text='clear_data')
@callback_check_authentication
async def clear(callback: types.CallbackQuery):
    msg_text = "Какие данные очистить?"
    await callback.message.edit_text(msg_text, reply_markup=clear_ikb)
    await Clear.command.set()


@dp.callback_query_handler(text=clear_list, state=Clear.command)
async def choose_command(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(command=callback.data)
    await callback.message.edit_text('Очистить данные?', reply_markup=clear_confirm_ikb)
    await Clear.delete.set()


@dp.callback_query_handler(text=['clear_yes'], state=Clear.delete)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(delete=callback.data)
    data = await state.get_data()
    await state.finish()
    keyboard = get_account_keyboard(str(callback.from_user.id))
    if del_all_data(data['command']):
        await callback.message.edit_text('Данные очищены.', reply_markup=clear_ikb)
        return
    await callback.message.edit_text('Произошла ошибка.', reply_markup=keyboard)