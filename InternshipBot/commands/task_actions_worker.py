from aiogram import types
from create import bot, dp
from aiogram.dispatcher import FSMContext
from commands.general import ConfirmDeletion, navigation, read_user_values, write_user_values, short_long_task
from commands.general import get_keyboard
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.commands import change_task, del_task, select_worker_task
from keyboard import change_task_ikb, task_worker_own_ikb, task_worker_without_del, \
    selected_task, task_worker_more_w_ikb, task_worker_more_without_del_w_ikb, back_task_own_ikb, del_task_worker_ikb


param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

change_param_task_list = list(param_task.keys())
globalDict_pagesW = read_user_values("globalDict_pagesW")


def get_worker_own_keyboard(s_id):
    k = task_worker_own_ikb
    if s_id is not None:
        k = task_worker_without_del
    return k


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
    tasks = select_worker_task(usr_id)

    if not tasks:
        keyboard = get_keyboard(usr_id)
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
        await callback.answer()
    else:
        count_tasks = len(tasks)

        if usr_id not in globalDict_pagesW:
            globalDict_pagesW[usr_id] = 0
            write_user_values("globalDict_pagesW", globalDict_pagesW)

        keyboard = get_worker_own_keyboard(tasks[globalDict_pagesW[usr_id]].student_id)

        if callback.data == 'worker_task':
            pw = globalDict_pagesW[usr_id]
            if globalDict_pagesW[usr_id] <= -1:
                pw = count_tasks + globalDict_pagesW[usr_id]
            count_tasks = len(tasks)
            await callback.message.edit_text(f"<b>№</b> {pw + 1}/{count_tasks}\n\n" + short_long_task(tasks[globalDict_pagesW[usr_id]]),
                                             parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
        else:
            s, globalDict_pagesW[usr_id] = navigation(callback.data, globalDict_pagesW[usr_id], count_tasks)
            write_user_values("globalDict_pagesW", globalDict_pagesW)
            keyboard = get_worker_own_keyboard(tasks[globalDict_pagesW[usr_id]].student_id)

            await callback.message.edit_text(s + short_long_task(tasks[globalDict_pagesW[usr_id]]), parse_mode='HTML',
                                             reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task_w')
async def show_more_worker_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи, опубликованной сотрудником.
    """
    tasks = select_worker_task(callback.from_user.id)
    usr_id = str(callback.from_user.id)

    keyboard = task_worker_more_w_ikb
    if tasks[globalDict_pagesW[usr_id]].student_id is not None:
        keyboard = task_worker_more_without_del_w_ikb
    await callback.message.edit_text(short_long_task(tasks[globalDict_pagesW[usr_id]], 1), parse_mode='HTML',
                                     reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='change_task_w')
async def ch_w_task(callback: types.CallbackQuery):
    """
    Функция возвращающая клавиатуру с доступными для изменения параметрами.
    """
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML',
                                  reply_markup=change_task_ikb)
    await TaskChangeW.param.set()


@dp.callback_query_handler(text=change_param_task_list, state=TaskChangeW.param)
async def ch_w_task_param(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для получения названия параметра, который пользователь желает изменить.
    """
    await state.update_data(param=callback.data)
    usr_id = str(callback.from_user.id)
    await state.update_data(num_task=globalDict_pagesW[usr_id])
    await callback.message.edit_text("Введите новое значение.")
    await TaskChangeW.next()


@dp.message_handler(state=TaskChangeW)
async def ch_w_task_val(message: types.Message, state=FSMContext):
    """
    Функция для получения нового значения параметра, который пользователь желает изменить.
    """
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b> {data['value']}\n\n", parse_mode='HTML')
    tasks = select_worker_task(message.from_user.id)
    t_id = tasks[data['num_task']].task_id
    name = tasks[data['num_task']].task_name
    change_task(t_id, data['param'][7:], data['value'])

    if tasks[data['num_task']].student_id is not None:
        s_id = tasks[data['num_task']].student_id
        await bot.send_message(s_id, f"В задаче <b><em>{name}</em></b> "
                                     f"параметр <b><em>{param_task.get(data['param'])}</em></b> был изменен на новое значение:"
                                     f"\n<b><em>{data['value']}</em></b>.",
                               reply_markup=selected_task, parse_mode='HTML')

    await message.answer('Задача изменена.', parse_mode='HTML', reply_markup=back_task_own_ikb)
    await state.finish()


@dp.callback_query_handler(text='del_task_w')
async def del_worker_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи сотрудника.
    """
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_worker_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_w_yes', state=ConfirmDeletion.delete)
async def del_worker_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи сотрудника.
    """
    await state.update_data(delete=callback.data)
    tasks = select_worker_task(callback.from_user.id)
    usr_id = str(callback.from_user.id)
    t_id = tasks[globalDict_pagesW[usr_id]].task_id
    count_tasks = len(tasks)
    del_task(t_id)

    if count_tasks is not None and (globalDict_pagesW[usr_id] >= count_tasks or globalDict_pagesW[usr_id] < count_tasks):
        globalDict_pagesW[usr_id] = 0
        write_user_values("globalDict_pagesW", globalDict_pagesW)

    await state.finish()
    await callback.message.edit_text('Задача удалена', parse_mode='HTML', reply_markup=back_task_own_ikb)

