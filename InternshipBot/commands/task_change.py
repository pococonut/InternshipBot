from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from commands.general import check_task_parameter
from create import bot, dp
from commands.task_actions import tasks_values
from commands.task_actions_worker import tasks_worker_values
from commands.get_menu import callback_check_authentication
from db.commands import select_task, change_task, get_user_type, select_worker_task
from keyboard import change_task_ikb, selected_task, back_task_w_ikb, back_task_own_ikb

param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

change_param_task_list = list(param_task.keys())
values_user_type = {}


class TaskChange(StatesGroup):
    num_task = State()
    param = State()
    value = State()


@dp.callback_query_handler(text=['change_task', 'change_task_worker'])
@callback_check_authentication
async def ch_task(callback: types.CallbackQuery):
    """
    Функция возвращающая клавиатуру с доступными для изменения параметрами.
    """

    if "worker" in callback.data:
        values_user_type[str(callback.from_user.id)] = callback.data

    msg_text = 'Выберите параметр который желаете изменить.'
    await callback.message.edit_text(msg_text, reply_markup=change_task_ikb)
    await TaskChange.param.set()


@dp.callback_query_handler(text=change_param_task_list, state=TaskChange.param)
async def choose_task_parameter(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для получения названия параметра, который пользователь желает изменить.
    """

    user_id = str(callback.from_user.id)
    user_type = get_user_type(user_id)[0]

    if user_type == 'worker' or user_id in values_user_type:
        page_task = tasks_worker_values[user_id]
    else:
        page_task = tasks_values[user_id]

    await state.update_data(param=callback.data)
    await state.update_data(num_task=page_task)
    await callback.message.edit_text("Введите новое значение.")
    await TaskChange.next()


@dp.message_handler(state=TaskChange.value)
async def change_task_value(message: types.Message, state=FSMContext):
    """
    Функция для получения нового значения параметра, который пользователь желает изменить.
    """

    await state.update_data(value=message.text)
    data = await state.get_data()

    if not check_task_parameter(data['param'], message.text):
        msg = 'Параметр введен в некорректном формате.'
        await message.answer(msg)
        return

    user_id = str(message.from_user.id)
    user_type = get_user_type(user_id)[0]

    if user_type == 'worker' or user_id in values_user_type:
        tasks = select_worker_task(user_id)
        keyboard = back_task_own_ikb
    else:
        tasks = select_task()
        keyboard = back_task_w_ikb

    if values_user_type.get(user_id):
        del values_user_type[user_id]

    task_id = tasks[data['num_task']].task_id
    task_name = tasks[data['num_task']].task_name
    change_task(task_id, data['param'][7:], data['value'])
    student_id = tasks[data['num_task']].student_id

    if student_id:
        msg_student = f"В задаче <b><em>{task_name}</em></b> " \
                      f"параметр <b><em>{param_task.get(data['param'])}" \
                      f"</em></b> был изменен на новое значение:" \
                      f"\n<b><em>{data['value']}</em></b>."

        for s_id in student_id.split(" "):
            await bot.send_message(s_id, msg_student, reply_markup=selected_task, parse_mode='HTML')

    msg_worker = f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n" \
                 f"<b>Новое значение:</b>\n{data['value']}\n\n" \
                 f"Задача изменена."

    await message.answer(msg_worker, parse_mode='HTML', reply_markup=keyboard)
    await state.finish()
