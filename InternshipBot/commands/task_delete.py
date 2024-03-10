from aiogram import types
from aiogram.dispatcher import FSMContext
from create import dp
from commands.task_actions import tasks_values
from commands.general import ConfirmDeletion, write_user_values
from db.commands import select_task, del_task
from keyboard import del_task_ikb, back_task_w_ikb


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