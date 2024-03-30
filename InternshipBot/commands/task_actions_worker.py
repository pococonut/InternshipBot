from aiogram import types
from create import dp
from commands.get_menu import callback_check_authentication
from commands.general import read_user_values
from commands.task_actions import get_task_message_keyboard, get_task_more_message

tasks_worker_values = read_user_values("tasks_worker_values")


@dp.callback_query_handler(text=['worker_task', 'worker_right', 'worker_left'])
@callback_check_authentication
async def show_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра задач, опубликованных сотрудником.
    """

    keyboard, msg_text = get_task_message_keyboard(callback, "tasks_worker_values", tasks_worker_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task_worker')
@callback_check_authentication
async def show_more_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи, опубликованной сотрудником.
    """

    keyboard, msg_text = get_task_more_message(callback, "tasks_worker_values", tasks_worker_values)
    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


