from aiogram import types
from create import dp
from commands.task_actions import get_task_message_keyboard
from commands.general import read_user_values, short_long_task
from db.commands import  select_worker_task
from keyboard import task_worker_more_w_ikb, task_worker_more_without_del_w_ikb

tasks_worker_values = read_user_values("tasks_worker_values")


@dp.callback_query_handler(text=['worker_task', 'worker_right', 'worker_left'])
async def show_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра задач, опубликованных сотрудником.
    """

    usr_id = str(callback.from_user.id)
    keyboard, msg_text = get_task_message_keyboard(usr_id, callback.data, "tasks_worker_values", tasks_worker_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task_w')
async def show_more_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи, опубликованной сотрудником.
    """

    usr_id = str(callback.from_user.id)
    tasks = select_worker_task(callback.from_user.id)
    current_task = tasks[tasks_worker_values[usr_id]]
    task_selected = current_task.student_id
    msg_text = short_long_task(current_task, 1)

    keyboard = task_worker_more_w_ikb
    if task_selected:
        keyboard = task_worker_more_without_del_w_ikb

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


