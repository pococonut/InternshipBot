from commands.back import back_func
from db.commands import user_type, add_task
from keyboard import admin_ikb, worker_ikb, back_ikb, back_cont_task_ikb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

# ------------------------- Добавление задачи -------------------------

FORM_task = """Для добавления новой задачи необходимо ввести:

<em>Название
Цель
Описание
Задачи
Необходимые навыки и технологии
Навыки и умения, получаемые в процессе прохождения практики
Количество людей
Материалы</em>

<b>отдельными сообщениями</b>.
"""


class Task(StatesGroup):
    task_name = State()
    task_goal = State()
    task_description = State()
    task_tasks = State()
    task_technologies = State()
    task_new_skills = State()
    num_people = State()
    materials = State()


async def add_t(callback: types.CallbackQuery):
    await callback.message.edit_text(FORM_task, parse_mode='HTML', reply_markup=back_cont_task_ikb)


async def cont_task_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите назание задачи.", parse_mode='HTML', reply_markup=back_ikb)
    await Task.task_name.set()


async def add_task_name(message: types.Message, state=FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer('Введите цель работы.')
    await Task.next()


async def add_task_goal(message: types.Message, state=FSMContext):
    await state.update_data(task_goal=message.text)
    await message.answer('Введите описание работы.')
    await Task.next()


async def add_task_description(message: types.Message, state=FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer('Введите задачи работы.')
    await Task.next()


async def add_task_tasks(message: types.Message, state=FSMContext):
    await state.update_data(task_tasks=message.text)
    await message.answer('Введите необходимые навыки и технологии.')
    await Task.next()


async def add_task_technologies(message: types.Message, state=FSMContext):
    await state.update_data(task_technologies=message.text)
    await message.answer('Введите навыки, получаемые в процессе проходения практики.')
    await Task.next()


async def add_task_new_skills(message: types.Message, state=FSMContext):
    await state.update_data(task_new_skills=message.text)
    await message.answer('Введите количество человек.')
    await Task.next()


async def add_task_num_people(message: types.Message, state=FSMContext):
    await state.update_data(num_people=message.text)
    await message.answer('Введите материалы.')
    await Task.next()


async def add_task_materials(message: types.Message, state=FSMContext):
    await state.update_data(materials=str(message.text))
    data = await state.get_data()
    task = add_task(message.from_id, data)
    if task:
        u_type = user_type(message.from_user.id)[0]
        keyboard = admin_ikb
        if u_type == 'worker':
            keyboard = worker_ikb
        await message.answer(f'📝 <b>Добавлена задача</b>\n\n'
                             f'<b>Название:</b> {data["task_name"]}\n\n'
                             f'<b>Цель:</b> {data["task_goal"]}\n\n'
                             f'<b>Описание:</b> {data["task_description"]}\n\n'
                             f'<b>Задачи:</b>\n{data["task_tasks"]}\n\n'
                             f'<b>Необходимые навыки и технологии:</b>\n{data["task_technologies"]}\n\n'
                             f'<b>Умения и навыки, получаемые в процессе прохождения практики:</b>\n{data["task_new_skills"]}\n\n'
                             f'<b>Количество людей:</b> {data["num_people"]}\n\n'
                             f'<b>Материалы:</b>\n{str(data["materials"])}', parse_mode='HTML',
                             reply_markup=keyboard, disable_web_page_preview=True)
        global page
        page = 0
    await state.finish()


def register_handlers_task_add(dp: Dispatcher):
    dp.register_callback_query_handler(add_t, text='add_task')
    dp.register_callback_query_handler(cont_task_command, text='continue_task', state="*")
    dp.register_message_handler(add_task_name, state=Task.task_name)
    dp.register_message_handler(add_task_goal, state=Task.task_goal)
    dp.register_message_handler(add_task_description, state=Task.task_description)
    dp.register_message_handler(add_task_tasks, state=Task.task_tasks)
    dp.register_message_handler(add_task_technologies, state=Task.task_technologies)
    dp.register_message_handler(add_task_new_skills, state=Task.task_new_skills)
    dp.register_message_handler(add_task_num_people, state=Task.num_people)
    dp.register_message_handler(add_task_materials, state=Task.materials)
    dp.register_callback_query_handler(back_func, text='back', state="*")