from commands.back import back_func
from commands.task_actions import ch_task_lst, short_long_task, param_task
from db.commands import user_type, change_task, del_task, select_worker_task
from keyboard import admin_ikb, worker_ikb, change_task_ikb, del_task_ikb, task_worker_own_ikb, task_worker_without_del, \
    back_to_tasks_w
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


# -------------------- Просмотр задач сотрудника --------------------

page_w = 0


async def show_worker_task(callback: types.CallbackQuery):
    global page_w
    # page_w = 0
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
        keyboard = task_worker_own_ikb

        pw = page_w
        count_tasks = len(tasks)
        if page_w <= -1:
            pw = count_tasks + page_w
        count_tasks = len(tasks)

        if tasks[page_w].student_id is not None:
            keyboard = task_worker_without_del
        await callback.message.edit_text(f"<b>№</b> {pw + 1}/{count_tasks}\n\n" + short_long_task(tasks[page_w]),
                                         parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


async def worker_rl(callback: types.CallbackQuery):
    global page_w
    tasks = select_worker_task(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.',
                                         reply_markup=task_worker_own_ikb)
    else:
        count_tasks = len(tasks)
        s = ''
        if callback.data == 'worker_right':
            page_w += 1
            if page_w == count_tasks:
                page_w = 0
            p_rw = page_w
            if page_w <= -1:
                p_rw = count_tasks + page_w
            s = f"<b>№</b> {p_rw + 1}/{count_tasks}\n\n"
        elif callback.data == 'worker_left':
            page_w -= 1
            p_lw = 0
            if page_w == (-1) * count_tasks:
                page_w = 0
            if page_w <= -1:
                p_lw = count_tasks
            s = f"<b>№</b> {(p_lw + page_w) + 1}/{count_tasks}\n\n"

        keyboard = task_worker_own_ikb
        if tasks[page_w].student_id is not None:
            keyboard = task_worker_without_del
        await callback.message.edit_text(s + short_long_task(tasks[page_w]), parse_mode='HTML', reply_markup=keyboard,
                                         disable_web_page_preview=True)


# -------------------- Подробный просмотр задачи сотрудника--------------------


async def show_more_worker_task(callback: types.CallbackQuery):
    tasks = select_worker_task(callback.from_user.id)
    await callback.message.edit_text(short_long_task(tasks[page_w], 1), parse_mode='HTML', reply_markup=back_to_tasks_w,
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
    await state.update_data(num_task=page_w)
    await callback.message.edit_text("Введите новое значение.")
    await TaskChangeW.next()


async def ch_w_task_val(message: types.Message, state=FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b> {data['value']}\n\n", parse_mode='HTML')
    tasks = select_worker_task(message.from_user.id)
    t_id = tasks[data['num_task']].task_id
    change_task(t_id, data['param'][7:], data['value'])
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
    global page_w
    await state.update_data(del_t=callback.data)
    tasks = select_worker_task(callback.from_user.id)
    t_id = tasks[page_w].task_id
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
