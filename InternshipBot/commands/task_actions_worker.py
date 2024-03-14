from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import bot, dp
from commands.task_actions import get_task_message_keyboard
from commands.general import ConfirmDeletion, read_user_values, write_user_values, short_long_task
from db.commands import change_task, del_task, select_worker_task
from keyboard import change_task_ikb, selected_task, task_worker_more_w_ikb, task_worker_more_without_del_w_ikb, \
    back_task_own_ikb, del_task_worker_ikb


param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

change_param_task_list = list(param_task.keys())
tasks_worker_values = read_user_values("tasks_worker_values")


class TaskChangeW(StatesGroup):
    num_task = State()
    param = State()
    value = State()


@dp.callback_query_handler(text=['worker_task', 'worker_right', 'worker_left'])
async def show_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра задач, опубликованных сотрудником.
    """

    usr_id = str(callback.from_user.id)
    keyboard, msg_text = get_task_message_keyboard(usr_id, callback.data, tasks_worker_values)
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


@dp.callback_query_handler(text='change_task_w')
async def ch_w_task(callback: types.CallbackQuery):
    """
    Функция возвращающая клавиатуру с доступными для изменения параметрами.
    """

    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите параметр который желаете изменить.', reply_markup=change_task_ikb)
    await TaskChangeW.param.set()


@dp.callback_query_handler(text=change_param_task_list, state=TaskChangeW.param)
async def ch_w_task_param(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для получения названия параметра, который пользователь желает изменить.
    """

    usr_id = str(callback.from_user.id)
    await state.update_data(param=callback.data)
    await state.update_data(num_task=tasks_worker_values[usr_id])
    await callback.message.edit_text("Введите новое значение.")
    await TaskChangeW.next()


@dp.message_handler(state=TaskChangeW)
async def ch_w_task_val(message: types.Message, state=FSMContext):
    """
    Функция для получения нового значения параметра, который пользователь желает изменить.
    """

    await state.update_data(value=message.text)
    data = await state.get_data()

    tasks = select_worker_task(message.from_user.id)
    task_id = tasks[data['num_task']].task_id
    task_name = tasks[data['num_task']].task_name
    student_id = tasks[data['num_task']].student_id
    change_task(task_id, data['param'][7:], data['value'])

    if student_id:
        msg_student = f"В задаче <b><em>{task_name}</em></b> "\
                      f"параметр <b><em>{param_task.get(data['param'])}" \
                      f"</em></b> был изменен на новое значение:"\
                      f"\n<b><em>{data['value']}</em></b>."
        await bot.send_message(student_id, msg_student, reply_markup=selected_task, parse_mode='HTML')

    msg_worker = f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n" \
                 f"<b>Новое значение:</b> {data['value']}\n\n" \
                 f"Задача изменена."
    await message.answer(msg_worker, parse_mode='HTML', reply_markup=back_task_own_ikb)
    await state.finish()


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

