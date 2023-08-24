from aiogram import types
from create import bot, dp
from aiogram.dispatcher import FSMContext
from commands.general import ConfirmDeletion, get_keyboard
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.commands import user_type, select_task_for_stud, select_task, select_already_get_stud,  change_task, \
    del_task, select_worker_reject, select_user
from keyboard import task_ikb, student_task_already_choose, student_task_choose, task_without_del, task_worker_ikb, \
    back_task_ikb, change_task_ikb, del_task_ikb, task_is_approve, selected_task, task_worker_more_ikb, \
    task_worker_more_without_del_ikb, task_student_more_ikb, task_worker_more_all, back_task_w_ikb


param_task = {'change_task_name': 'Название',
              'change_task_goal': 'Цель',
              'change_task_description': 'Описание',
              'change_task_tasks': 'Задачи',
              'change_task_technologies': 'Навыки и технологии',
              'change_task_new_skills': 'Получаемые навыки',
              'change_num_people': 'Количество людей',
              'change_materials': 'Материалы'}

ch_task_lst = list(param_task.keys())

globalDict_pages = dict()


class TaskChange(StatesGroup):
    num_task = State()
    param = State()
    value = State()


def short_long_task(t, f=0):
    """
    Функция вывода данных задачи.
    :param t: Строка модели БД, относящаяся к конкретной задаче, с информацией о ней.
    :param f: Булево значение, 1 - вывод всей информации задачи, 0 - вывод краткой информации задачи.
    :return: Строка с информацией о задаче.
    """
    s = f"<b>Название:</b> {t.task_name}\n\n" \
        f"<b>Цель:</b> {t.task_goal}\n\n" \
        f"<b>Описание:</b> {t.task_description}\n\n" \
        f"<b>Необходимые навыки и технологии:</b>\n{t.task_technologies}\n\n"
    if f == 1:
        s += f"<b>Задачи:</b>\n{t.task_tasks}\n\n" \
             f"<b>Умения и навыки, получаемые в процессе прохождения практики:</b>\n{t.task_new_skills}\n\n" \
             f"<b>Количество людей:</b> {t.num_people}\n\n" \
             f"<b>Материалы:</b>\n{str(t.materials)}\n\n"

    if select_user(t.from_id):
        s += f"<b>Сотрудник:</b> <a href='tg://user?id={t.from_id}'>{select_user(t.from_id).name}</a>"

    return s


def get_keyboard_task(user, have_task, t_id):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param user: Тип пользователя (Студент, Администратор, Директор, Сотрудник).
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """
    k = task_ikb
    if user == 'student':
        already_get = select_already_get_stud(t_id)
        if already_get:
            k = student_task_already_choose
        else:
            k = student_task_choose
    elif user in ('admin', 'director'):
        k = task_ikb
        if have_task is not None:
            k = task_without_del
    elif user == 'worker':
        k = task_worker_ikb
    return k


@dp.callback_query_handler(text=['show_task', 'right', 'left'])
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """
    u_type = user_type(callback.from_user.id)[0]
    usr_id = str(callback.from_user.id)

    if u_type == 'student':
        tasks = select_task_for_stud()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = get_keyboard(usr_id)
        await callback.message.edit_text('В данный момент задач нет.\nЗагляните позже.', reply_markup=keyboard)
        await callback.answer()
    else:
        if usr_id not in globalDict_pages:
            globalDict_pages[usr_id] = 0

        count_tasks = len(tasks)
        keyboard = get_keyboard_task(u_type, tasks[globalDict_pages[usr_id]].student_id, usr_id)

        if callback.data == 'show_task':
            print(globalDict_pages)
            count_tasks = len(tasks)
            p = globalDict_pages[usr_id]

            if globalDict_pages[usr_id] <= -1:
                p = count_tasks + globalDict_pages[usr_id]

            await callback.message.edit_text(
                f"<b>№</b> {p + 1}/{count_tasks}\n\n" + short_long_task(tasks[globalDict_pages[usr_id]]),
                parse_mode='HTML',
                reply_markup=keyboard,
                disable_web_page_preview=True)
        else:
            if callback.data == 'right':

                globalDict_pages[usr_id] += 1
                if globalDict_pages[usr_id] == count_tasks:
                    globalDict_pages[usr_id] = 0
                p_r = globalDict_pages[usr_id]
                if globalDict_pages[usr_id] <= -1:
                    p_r = count_tasks + globalDict_pages[usr_id]
                s = f"<b>№</b> {p_r + 1}/{count_tasks}\n\n"

            elif callback.data == 'left':
                globalDict_pages[usr_id] -= 1
                p_l = 0
                if globalDict_pages[usr_id] == (-1) * count_tasks:
                    globalDict_pages[usr_id] = 0
                if globalDict_pages[usr_id] <= -1:
                    p_l = count_tasks
                s = f"<b>№</b> {(p_l + globalDict_pages[usr_id]) + 1}/{count_tasks}\n\n"
            print(globalDict_pages)
            await callback.message.edit_text(s + short_long_task(tasks[globalDict_pages[usr_id]]),
                                             parse_mode='HTML',
                                             reply_markup=keyboard,
                                             disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task')
async def show_more_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи.
    """
    u_type = user_type(callback.from_user.id)[0]
    usr_id = str(callback.from_user.id)
    if u_type == 'student':
        tasks = select_task_for_stud()
        keyboard = task_student_more_ikb
    else:
        tasks = select_task()

        if u_type == 'worker':
            keyboard = task_worker_more_all
        else:
            keyboard = task_worker_more_ikb
            if tasks[globalDict_pages[usr_id]].student_id is not None:
                keyboard = task_worker_more_without_del_ikb

    await callback.message.edit_text(short_long_task(tasks[globalDict_pages[usr_id]], 1), parse_mode='HTML',
                                     reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='change_task')
async def ch_task(callback: types.CallbackQuery):
    """
    Функция возвращающая клавиатуру с доступными для изменения параметрами.
    """
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите параметр который желаете изменить.', reply_markup=change_task_ikb)
    await TaskChange.param.set()


@dp.callback_query_handler(text=ch_task_lst, state=TaskChange.param)
async def ch_task_param(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для получения названия параметра, который пользователь желает изменить.
    """
    await state.update_data(param=callback.data)
    usr_id = str(callback.from_user.id)
    await state.update_data(num_task=globalDict_pages[usr_id])
    await callback.message.edit_text("Введите новое значение.")
    await TaskChange.next()


@dp.message_handler(state=TaskChange.value)
async def ch_task_val(message: types.Message, state=FSMContext):
    """
    Функция для получения нового значения параметра, который пользователь желает изменить.
    """
    await state.update_data(value=message.text)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                         f"<b>Новое значение:</b>\n{data['value']}\n\n", parse_mode='HTML')
    tasks = select_task()
    t_id = tasks[data['num_task']].task_id
    name = tasks[data['num_task']].task_name
    change_task(t_id, data['param'][7:], data['value'])
    if tasks[data['num_task']].student_id is not None:
        s_id = tasks[data['num_task']].student_id
        await bot.send_message(s_id, f"В задаче <b><em>{name}</em></b> "
                                     f"параметр <b><em>{param_task.get(data['param'])}</em></b> был изменен на новое значение:"
                                     f"\n<b><em>{data['value']}</em></b>.",
                               reply_markup=selected_task, parse_mode='HTML')

    if user_type(message.from_user.id)[0] == 'student':
        keyboard = back_task_ikb
    else:
        keyboard = back_task_w_ikb
    await message.answer('Задача изменена.', parse_mode='HTML', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='del_task')
async def del_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи.
    """
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить задачу?', parse_mode='HTML', reply_markup=del_task_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_yes', state=ConfirmDeletion.delete)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи.
    """
    await state.update_data(delete=callback.data)
    tasks = select_task()
    usr_id = str(callback.from_user.id)
    t_id = tasks[globalDict_pages[usr_id]].task_id
    del_task(t_id)
    await state.finish()
    await callback.message.edit_text('Задача удалена', parse_mode='HTML', reply_markup=back_task_w_ikb)


@dp.callback_query_handler(text='stud_get_task')
async def stud_get_task(callback: types.CallbackQuery):
    """
    Функция для фиксирования выбора задачи студентом.
    """
    tasks = select_task_for_stud()
    usr_id = str(callback.from_user.id)
    t_id = tasks[globalDict_pages[usr_id]].task_id
    worker_id = tasks[globalDict_pages[usr_id]].from_id
    change_task(t_id, 'student_id', callback.from_user.id)
    task_name = select_worker_reject(callback.from_user.id).task_name
    student_name = select_user(callback.from_user.id).name
    await bot.send_message(worker_id, f'Студент\ка <a href="tg://user?id={callback.from_user.id}">{student_name}</a> '
                                      f'<b>выбрал\а</b> задачу <em>{task_name}</em>.',
                           reply_markup=task_is_approve, parse_mode='HTML')
    await callback.message.edit_text(f'Задача <em>{task_name}</em> выбрана.\nВы можете отказаться от задачи,'
                                     f' нажав в меню <em>Выбранная задача</em>.',
                                     parse_mode='HTML', reply_markup=back_task_ikb)
