from aiogram import types
from aiogram.dispatcher import FSMContext
from commands.task_actions_worker import tasks_worker_values
from create import dp
from commands.task_actions import tasks_values
from commands.general import ConfirmDeletion, write_user_values
from db.commands import select_task, del_task, select_worker_task
from keyboard import del_task_ikb, back_task_w_ikb, back_task_own_ikb, del_task_worker_ikb


@dp.callback_query_handler(text='del_task')
async def del_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи.
    """

    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить задачу?', reply_markup=del_task_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_yes', state=ConfirmDeletion.delete)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи.
    """

    await state.update_data(delete=callback.data)
    tasks = select_task()
    usr_id = str(callback.from_user.id)
    task_id = tasks[tasks_values[usr_id]].task_id
    count_tasks = len(tasks)
    del_task(task_id)

    wrong_page_1 = tasks_values[usr_id] >= count_tasks
    wrong_page_2 = tasks_values[usr_id] < count_tasks
    if count_tasks and (wrong_page_1 or wrong_page_2):
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    await state.finish()
    await callback.message.edit_text('Задача удалена.', reply_markup=back_task_w_ikb)


@dp.callback_query_handler(text='del_task_w')
async def del_worker_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи сотрудника.
    """

    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить задачу?', reply_markup=del_task_worker_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_w_yes', state=ConfirmDeletion.delete)
async def del_worker_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи сотрудника.
    """

    await state.update_data(delete=callback.data)
    usr_id = str(callback.from_user.id)
    tasks = select_worker_task(usr_id)
    task_id = tasks[tasks_worker_values[usr_id]].task_id
    count_tasks = len(tasks)
    del_task(task_id)
    await state.finish()

    condition1 = tasks_worker_values[usr_id] >= count_tasks
    condition2 = tasks_worker_values[usr_id] < count_tasks
    if count_tasks and (condition1 or condition2):
        tasks_worker_values[usr_id] = 0
        write_user_values("tasks_worker_values", tasks_worker_values)

    msg_text = 'Задача удалена.'
    await callback.message.edit_text(msg_text, reply_markup=back_task_own_ikb)
