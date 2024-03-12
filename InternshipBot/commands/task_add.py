from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from db.commands import user_type, add_task
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard import admin_ikb, worker_ikb, back_ikb, back_cont_task_ikb


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


@dp.callback_query_handler(text='add_task')
async def add_t(callback: types.CallbackQuery):
    await callback.message.edit_text(FORM_task, parse_mode='HTML', reply_markup=back_cont_task_ikb)


@dp.callback_query_handler(text='continue_task', state="*")
async def cont_task_command(callback: types.CallbackQuery):
    """
    Функция начала ввода параметров задачи.
    """

    await callback.message.edit_text("Введите название задачи.", reply_markup=back_ikb)
    await Task.task_name.set()


@dp.message_handler(state=Task.task_name)
async def add_task_name(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Название.
    """

    if len(message.text.split()) > 50:
        msg_text = 'Количество слов параметра <em>Название</em> превышает максимальное значение - 50 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_name=message.text)
    await message.answer('Введите цель работы.')
    await Task.next()


@dp.message_handler(state=Task.task_goal)
async def add_task_goal(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Цель задачи.
    """

    if len(message.text.split()) > 50:
        msg_text = 'Количество слов параметра <em>Цель задачи</em> превышает максимальное значение - 50 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_goal=message.text)
    await message.answer('Введите описание работы.')
    await Task.next()


@dp.message_handler(state=Task.task_description)
async def add_task_description(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Описание задачи.
    """

    if len(message.text.split()) > 200:
        msg_text = 'Количество слов параметра <em>Описание задачи</em> превышает максимальное значение - 200 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_description=message.text)
    await message.answer('Введите задачи работы.')
    await Task.next()


@dp.message_handler(state=Task.task_tasks)
async def add_task_tasks(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Подзадачи.
    """

    if len(message.text.split()) > 500:
        msg_text = 'Количество слов параметра <em>Описание задачи</em> превышает максимальное значение - 500 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_tasks=message.text)
    await message.answer('Введите необходимые навыки и технологии.')
    await Task.next()


@dp.message_handler(state=Task.task_technologies)
async def add_task_technologies(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Необходимые навыки и технологии.
    """

    if len(message.text.split()) > 200:
        msg_text = 'Количество слов параметра <em>Навыки и технологии</em> превышает максимальное значение - 200 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_technologies=message.text)
    await message.answer('Введите навыки, получаемые в процессе прохождения практики.')
    await Task.next()


@dp.message_handler(state=Task.task_new_skills)
async def add_task_new_skills(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Навыки, получаемые в процессе прохождения практики.
    """

    if len(message.text.split()) > 200:
        msg_text = 'Количество слов параметра <em>Получаемые навыки</em> превышает максимальное значение - 200 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(task_new_skills=message.text)
    await message.answer('Введите количество человек.')
    await Task.next()


@dp.message_handler(state=Task.num_people)
async def add_task_num_people(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Количество человек.
    """

    if len(message.text.split()) > 1 or any(chr.isalpha() for chr in message.text):
        await message.answer('Параметр введен в некорректном формате. Повторите ввод')
        return

    if int(message.text) > 5:
        await message.answer('Количество человек превышает максимальное значение - 5 человек.')
        return

    await state.update_data(num_people=message.text)
    await message.answer('Введите материалы.')
    await Task.next()


@dp.message_handler(state=Task.materials)
async def add_task_materials(message: types.Message, state=FSMContext):
    """
    Функция получения параметра задачи - Материалы.
    """

    if len(message.text.split()) > 200:
        msg_text = 'Количество слов параметра <em>Материалы</em> превышает максимальное значение - 200 слов'
        await message.answer(msg_text, parse_mode='HTML')
        return

    await state.update_data(materials=str(message.text))
    data = await state.get_data()
    task = add_task(message.from_id, data)

    if task:
        u_type = user_type(message.from_user.id)[0]
        keyboard = worker_ikb if u_type == 'worker' else admin_ikb
        msg_text = f'📝 <b>Добавлена задача</b>\n\n' \
                   f'<b>Название:</b> {data["task_name"]}\n\n' \
                   f'<b>Цель:</b> {data["task_goal"]}\n\n' \
                   f'<b>Описание:</b> {data["task_description"]}\n\n' \
                   f'<b>Задачи:</b>\n{data["task_tasks"]}\n\n' \
                   f'<b>Необходимые навыки и технологии:</b>\n{data["task_technologies"]}\n\n' \
                   f'<b>Навыки, получаемые в процессе прохождения практики:</b>\n{data["task_new_skills"]}\n\n' \
                   f'<b>Количество людей:</b> {data["num_people"]}\n\n' \
                   f'<b>Материалы:</b>\n{str(data["materials"])}'
        await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
    await state.finish()
