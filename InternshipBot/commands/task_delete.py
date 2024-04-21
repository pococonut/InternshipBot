from aiogram import types
from aiogram.dispatcher import FSMContext

from create import dp
from db.commands import del_task
from commands.general import ConfirmDeletion
from commands.get_keyboard import get_keyboard_deletion
from commands.get_menu import callback_check_authentication
from commands.task_actions_worker import tasks_worker_values
from commands.task_actions import tasks_values, check_range, get_tasks_for_user
from keyboard import back_task_w_ikb, back_task_own_ikb


def get_values_deletion(callback):
    """
    Функция для получения значений навигации и клавиатуры при удалении задачи
    :param callback: Кнопка
    :return: Значения навигации и клавиатура
    """

    if 'worker' in callback:
        return tasks_worker_values, "tasks_worker_values", back_task_own_ikb
    return tasks_values, "tasks_values", back_task_w_ikb


@dp.callback_query_handler(text=['del_task', 'del_task_worker'])
@callback_check_authentication
async def del_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи.
    """

    keyboard = get_keyboard_deletion(callback.data)
    await callback.message.edit_text('Удалить задачу?', reply_markup=keyboard)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text=['del_yes', 'del_yes_worker'], state=ConfirmDeletion.delete)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи.
    """

    values, name_values, keyboard = get_values_deletion(callback.data)
    await state.update_data(delete=callback.data)
    usr_id = str(callback.from_user.id)
    tasks = get_tasks_for_user(usr_id, callback.data)
    task_id = tasks[values[usr_id]].task_id
    del_task(task_id)
    await state.finish()

    count_tasks = len(tasks)
    msg_text = 'Задача удалена.'
    check_range(count_tasks, usr_id, name_values, values)
    await callback.message.edit_text(msg_text, reply_markup=keyboard)
