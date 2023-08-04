from commands.back import back_func
from commands.task_actions import ch_task_lst, param_task
from create import bot
from db.commands import user_type, change_task, del_task, select_worker_task
from keyboard import admin_ikb, worker_ikb, change_task_ikb, del_task_ikb, task_worker_own_ikb, task_worker_without_del, \
    back_to_tasks_w, selected_task, task_worker_more_w_ikb, task_worker_more_without_del_w_ikb
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


# -------------------- Просмотр задач сотрудника --------------------

globalDict_pagesW = dict()


def short_long_task(t, f=0):
    if f == 1:
        s = f"<b>Название:</b> {t.task_name}\n\n" \
            f"<b>Цель:</b> {t.task_goal}\n\n" \
            f"<b>Описание:</b> {t.task_description}\n\n" \
            f"<b>Задачи:</b>\n{t.task_tasks}\n\n" \
            f"<b>Необходимые навыки и технологии:</b>\n{t.task_technologies}\n\n" \
            f"<b>Умения и навыки, получаемые в процессе прохождения практики:</b>\n{t.task_new_skills}\n\n" \
            f"<b>Количество людей:</b> {t.num_people}\n\n" \
            f"<b>Материалы:</b>\n{str(t.materials)}"
    else:
        s = f"<b>Название:</b> {t.task_name}\n\n" \
            f"<b>Цель:</b> {t.task_goal}\n\n" \
            f"<b>Описание:</b> {t.task_description}\n\n" \
            f"<b>Необходимые навыки и технологии:</b>\n{t.task_technologies}\n\n"
    return s


async def show_worker_task(callback: types.CallbackQuery):
    tasks = select_worker_task(callback.from_user.id)

    if not tasks:
        keyboard = admin_ikb
        if user_type(callback.from_user.id)[0] == 'worker':
            keyboard = worker_ikb
        try:
            await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.',
                                             reply_markup=keyboard)
        except:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент задач нет.\nЗагляните позже.',
                                          reply_markup=keyboard)
    else:
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_pagesW:
            globalDict_pagesW[usr_id] = 0
        print(globalDict_pagesW)

        keyboard = task_worker_own_ikb

        pw = globalDict_pagesW[usr_id]
        count_tasks = len(tasks)
        if globalDict_pagesW[usr_id] <= -1:
            pw = count_tasks + globalDict_pagesW[usr_id]
        count_tasks = len(tasks)

        if tasks[globalDict_pagesW[usr_id]].student_id is not None:
            keyboard = task_worker_without_del
        await callback.message.edit_text(f"<b>№</b> {pw + 1}/{count_tasks}\n\n" + short_long_task(tasks[globalDict_pagesW[usr_id]]),
                                         parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


async def worker_rl(callback: types.CallbackQuery):
    tasks = select_worker_task(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.',
                                         reply_markup=task_worker_own_ikb)
    else:
        count_tasks = len(tasks)
        s = ''
        usr_id = str(callback.from_user.id)
        if usr_id not in globalDict_pagesW:
            globalDict_pagesW[usr_id] = 0

        if callback.data == 'worker_right':
            globalDict_pagesW[usr_id] += 1
            if globalDict_pagesW[usr_id] == count_tasks:
                globalDict_pagesW[usr_id] = 0
            p_rw = globalDict_pagesW[usr_id]
            if globalDict_pagesW[usr_id] <= -1:
                p_rw = count_tasks + globalDict_pagesW[usr_id]
            s = f"<b>№</b> {p_rw + 1}/{count_tasks}\n\n"
        elif callback.data == 'worker_left':
            globalDict_pagesW[usr_id] -= 1
            p_lw = 0
            if globalDict_pagesW[usr_id] == (-1) * count_tasks:
                globalDict_pagesW[usr_id] = 0
            if globalDict_pagesW[usr_id] <= -1:
                p_lw = count_tasks
            s = f"<b>№</b> {(p_lw + globalDict_pagesW[usr_id]) + 1}/{count_tasks}\n\n"

        keyboard = task_worker_own_ikb
        if tasks[globalDict_pagesW[usr_id]].student_id is not None:
            keyboard = task_worker_without_del

        print(globalDict_pagesW)
        await callback.message.edit_text(s + short_long_task(tasks[globalDict_pagesW[usr_id]]), parse_mode='HTML', reply_markup=keyboard,
                                         disable_web_page_preview=True)


# -------------------- Подробный просмотр задачи сотрудника--------------------


async def show_more_worker_task(callback: types.CallbackQuery):
    tasks = select_worker_task(callback.from_user.id)
    usr_id = str(callback.from_user.id)

    keyboard = task_worker_more_w_ikb
    if tasks[globalDict_pagesW[usr_id]].student_id is not None:
        keyboard = task_worker_more_without_del_w_ikb
    await callback.message.edit_text(short_long_task(tasks[globalDict_pagesW[usr_id]], 1), parse_mode='HTML', reply_markup=keyboard,
                                     disable_web_page_preview=True)


# -------------------- Изменение параметров задачи сотрудника--------------------


class TaskChangeW(StatesGroup):
    num_task = State()
    param = State()
    value = State()


async def ch_w_task(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML',
                                  reply_markup=change_task_ikb)
    await TaskChangeW.param.set()


async def ch_w_task_param(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(param=callback.data)
    usr_id = str(callback.from_user.id)
    await state.update_data(num_task=globalDict_pagesW[usr_id])
    await callback.message.edit_text("Введите новое значение.")
    await TaskChangeW.next()


async def ch_w_task_val(message: types.Message, state=FSMContext):
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

    await message.answer('Задача изменена.', parse_mode='HTML', reply_markup=back_to_tasks_w)
    await state.finish()


# ---------------------- Удаление задачи сотрудника ----------------------


class TaskDelW(StatesGroup):
    del_t = State()


async def del_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await TaskDelW.del_t.set()


async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(del_t=callback.data)
    tasks = select_worker_task(callback.from_user.id)
    usr_id = str(callback.from_user.id)
    t_id = tasks[globalDict_pagesW[usr_id]].task_id
    del_task(t_id)
    await state.finish()
    await callback.message.edit_text('Задача удалена', parse_mode='HTML', reply_markup=back_to_tasks_w)


def register_handlers_task_actions_worker(dp: Dispatcher):
    dp.register_callback_query_handler(show_worker_task, text='worker_task')
    dp.register_callback_query_handler(worker_rl, text=['worker_right', 'worker_left'])
    dp.register_callback_query_handler(show_more_worker_task, text='more_task_w')
    dp.register_callback_query_handler(ch_w_task, text='change_task_w')
    dp.register_callback_query_handler(ch_w_task_param, text=ch_task_lst, state=TaskChangeW.param)
    dp.register_message_handler(ch_w_task_val, state=TaskChangeW)
    dp.register_callback_query_handler(del_t, text='del_task_w')
    dp.register_callback_query_handler(del_t_yes, text='del_yes', state=TaskDelW.del_t)
    dp.register_callback_query_handler(back_func, text='back', state="*")
