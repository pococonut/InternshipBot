from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import bot, dp
from commands.task_actions import tasks_values
from db.commands import select_task, change_task, user_type
from keyboard import change_task_ikb, selected_task, back_task_ikb, back_task_w_ikb

param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

change_param_task_list = list(param_task.keys())


class TaskChange(StatesGroup):
    num_task = State()
    param = State()
    value = State()


@dp.callback_query_handler(text='change_task')
async def ch_task(callback: types.CallbackQuery):
    """
    Функция возвращающая клавиатуру с доступными для изменения параметрами.
    """

    await callback.message.edit_reply_markup()
    msg_text = 'Выберите параметр который желаете изменить.'
    await callback.message.edit_text(msg_text, reply_markup=change_task_ikb)
    await TaskChange.param.set()


@dp.callback_query_handler(text=change_param_task_list, state=TaskChange.param)
async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для получения названия параметра, который пользователь желает изменить.
    """

    await state.update_data(param=callback.data)
    usr_id = str(callback.from_user.id)
    await state.update_data(num_task=tasks_values[usr_id])
    await callback.message.edit_text("Введите новое значение.")
    await TaskChange.next()


@dp.message_handler(state=TaskChange.value)
async def ch_task_val(message: types.Message, state=FSMContext):
    """
    Функция для получения нового значения параметра, который пользователь желает изменить.
    """

    user_id = str(message.from_user.id)

    await state.update_data(value=message.text)
    data = await state.get_data()

    tasks = select_task()
    task_id = tasks[data['num_task']].task_id
    task_name = tasks[data['num_task']].task_name
    change_task(task_id, data['param'][7:], data['value'])

    task_with_student = tasks[data['num_task']].student_id
    if task_with_student:
        msg_text = (f"В задаче <b><em>{task_name}</em></b> параметр "
                    f"<b><em>{param_task.get(data['param'])}</em></b> "
                    f"был изменен на новое значение:\n<b><em>{data['value']}</em></b>.")
        student_id = tasks[data['num_task']].student_id
        await bot.send_message(student_id, msg_text, reply_markup=selected_task, parse_mode='HTML')

    if user_type(user_id)[0] == 'student':
        keyboard = back_task_ikb
    else:
        keyboard = back_task_w_ikb

    msg_text = (f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                f"<b>Новое значение:</b>\n{data['value']}\n\n"
                f"Задача изменена.")
    await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard)
    await state.finish()