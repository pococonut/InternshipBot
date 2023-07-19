from commands.back import back_func
from db.commands import user_type, select_task_for_stud, select_task, select_already_get_stud, \
    change_task, del_task, select_worker_reject
from keyboard import admin_ikb, worker_ikb, stud_is_approve, task_ikb, student_task_already_choose, \
    student_task_choose, task_without_del, task_worker_ikb, back_task_ikb, change_task_ikb, del_task_ikb, \
    task_is_approve
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from create import bot

# -------------------- Просмотр всех задач --------------------

page = 0


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


async def show_task(callback: types.CallbackQuery):
    global page
    # page = 0
    u_type = user_type(callback.from_user.id)[0]

    if u_type == 'student':
        tasks = select_task_for_stud()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = admin_ikb
        if u_type == 'worker':
            keyboard = worker_ikb
        elif u_type == 'student':
            keyboard = stud_is_approve
        try:
            await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
        except:
            await callback.message.edit_reply_markup()
            await callback.message.delete()
            await callback.message.answer('В данный момент задач нет.\nЗагляните позже.',
                                          reply_markup=keyboard)
    else:

        keyboard = task_ikb
        if u_type == 'student':
            already_get = select_already_get_stud(callback.from_user.id)
            if already_get:
                keyboard = student_task_already_choose
            else:
                keyboard = student_task_choose
        elif u_type in ('admin', 'director'):
            keyboard = task_ikb
            if tasks[page].student_id is not None:
                keyboard = task_without_del
        elif u_type == 'worker':
            keyboard = task_worker_ikb

        p = page
        count_tasks = len(tasks)
        if page <= -1:
            p = count_tasks + page
        count_tasks = len(tasks)
        await callback.message.edit_text(f"<b>№</b> {p + 1}/{count_tasks}\n\n" + short_long_task(tasks[page]),
                                         parse_mode='HTML',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)


async def show_task_rl(callback: types.CallbackQuery):
    global page

    u_type = user_type(callback.from_user.id)[0]
    if u_type == 'student':
        tasks = select_task_for_stud()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = admin_ikb
        if u_type == 'worker':
            keyboard = worker_ikb
        elif u_type == 'student':
            keyboard = stud_is_approve
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
    else:
        count_tasks = len(tasks)
        s = ''
        if callback.data == 'right':
            page += 1
            if page == count_tasks:
                page = 0
            p_r = page
            if page <= -1:
                p_r = count_tasks + page
            s = f"<b>№</b> {p_r + 1}/{count_tasks}\n\n"

        if callback.data == 'left':
            page -= 1
            p_l = 0
            if page == (-1) * count_tasks:
                page = 0
            if page <= -1:
                p_l = count_tasks
            s = f"<b>№</b> {(p_l + page) + 1}/{count_tasks}\n\n"

        keyboard = task_ikb
        if u_type == 'student':
            already_get = select_already_get_stud(callback.from_user.id)
            if already_get:
                keyboard = student_task_already_choose
            else:
                keyboard = student_task_choose
        elif u_type in ('admin', 'director'):
            keyboard = task_ikb
            if tasks[page].student_id is not None:
                keyboard = task_without_del
        elif u_type == 'worker':
            keyboard = task_worker_ikb

        await callback.message.edit_text(s + short_long_task(tasks[page]),
                                         parse_mode='HTML',
                                         reply_markup=keyboard,
                                         disable_web_page_preview=True)


# -------------------- Подробный просмотр задачи --------------------


async def show_more_task(callback: types.CallbackQuery):
    u_type = user_type(callback.from_user.id)[0]
    if u_type == 'student':
        tasks = select_task_for_stud()
    else:
        tasks = select_task()
    await callback.message.edit_text(short_long_task(tasks[page], 1), parse_mode='HTML', reply_markup=back_task_ikb,
                                     disable_web_page_preview=True)


# -------------------- Изменение параметров задачи --------------------


class TaskChange(StatesGroup):
    num_task = State()
    param = State()
    value = State()


param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

ch_task_lst = list(param_task.keys())


async def ch_task(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    print("change", page + 1)
    await callback.message.answer('Выберите параметр который желаете изменить.', parse_mode='HTML', reply_markup=change_task_ikb)
    await TaskChange.param.set()


async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(param=callback.data)
    await state.update_data(num_task=page)
    await callback.message.edit_text("Введите новое значение.")
    await TaskChange.next()


async def ch_task_val(message: types.Message, state=FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b>\n{data['value']}\n\n", parse_mode='HTML')
    tasks = select_task()
    t_id = tasks[data['num_task']].task_id
    change_task(t_id, data['param'][7:], data['value'])
    await message.answer('Задача изменена.', parse_mode='HTML', reply_markup=back_task_ikb)
    await state.finish()


# ---------------------- Удаление задачи ----------------------


class TaskDel(StatesGroup):
    del_t = State()


async def del_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    print("delite ", page + 1)
    await callback.message.answer('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await TaskDel.del_t.set()


async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    global page
    await state.update_data(del_t=callback.data)
    tasks = select_task()
    t_id = tasks[page].task_id
    del_task(t_id)
    await state.finish()
    #page -= 1
    await callback.message.edit_text('Задача удалена', parse_mode='HTML', reply_markup=back_task_ikb)


# ----------------- Выбор задачи студентом -----------------


async def stud_get_task(callback: types.CallbackQuery):
    global page
    tasks = select_task_for_stud()
    t_id = tasks[page].task_id
    worker_id = tasks[page].from_id
    print(page, worker_id)
    change_task(t_id, 'student_id', callback.from_user.id)
    task_name = select_worker_reject(callback.from_user.id).task_name

    await bot.send_message(worker_id, f'Задача <em>{task_name}</em> была <b>выбранна</b> студентом.\n\n',
                           reply_markup=task_is_approve, parse_mode='HTML')
    await callback.message.edit_text('Задача выбрана.\nВы можете отказаться от задачи,'
                                     ' нажав в меню <em>Выбранная задача</em>.',
                                     parse_mode='HTML', reply_markup=back_task_ikb)


def register_handlers_task_actions(dp: Dispatcher):
    dp.register_callback_query_handler(show_task, text='show_task')
    dp.register_callback_query_handler(show_task_rl, text=['right', 'left'])
    dp.register_callback_query_handler(show_more_task, text='more_task')
    dp.register_callback_query_handler(ch_task, text='change_task')
    dp.register_callback_query_handler(ch_task_param, text=ch_task_lst, state=TaskChange.param)
    dp.register_message_handler(ch_task_val, state=TaskChange.value)
    dp.register_callback_query_handler(del_t, text='del_task')
    dp.register_callback_query_handler(del_t_yes, text='del_yes', state=TaskDel.del_t)
    dp.register_callback_query_handler(stud_get_task, text='stud_get_task')
    dp.register_callback_query_handler(back_func, text='back', state="*")





