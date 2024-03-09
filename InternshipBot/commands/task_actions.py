from aiogram import types
from create import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from commands.general import ConfirmDeletion, get_keyboard, navigation, read_user_values, write_user_values
from db.commands import user_type, select_task, select_already_get_stud, change_task, del_task, select_user
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

change_param_task_list = list(param_task.keys())
tasks_values = read_user_values("tasks_values")


class TaskChange(StatesGroup):
    num_task = State()
    param = State()
    value = State()


def short_long_task(task, flag=0):
    """
    Функция вывода данных задачи.
    :param task: Строка модели БД, относящаяся к конкретной задаче, с информацией о ней.
    :param flag: Булево значение, 1 - вывод всей информации задачи, 0 - вывод краткой информации задачи.
    :return: Строка с информацией о задаче.
    """

    s = f"<b>Название:</b> {task.task_name}\n\n" \
        f"<b>Цель:</b> {task.task_goal}\n\n" \
        f"<b>Описание:</b> {task.task_description}\n\n" \
        f"<b>Необходимые навыки и технологии:</b>\n{task.task_technologies}\n\n"

    if flag:
        s += f"<b>Задачи:</b>\n{task.task_tasks}\n\n" \
             f"<b>Умения и навыки, получаемые в процессе " \
             f"прохождения практики:</b>\n{task.task_new_skills}\n\n" \
             f"<b>Количество людей:</b> {task.num_people}\n\n" \
             f"<b>Материалы:</b>\n{str(task.materials)}\n\n"

    if select_user(task.from_id):
        s += f"<b>Сотрудник:</b> <a href='tg://user?id={task.from_id}'>{select_user(task.from_id).name}</a>"

    return s


def get_keyboard_task(usr_type, have_task, task_id):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param usr_type: Тип пользователя (Студент, Администратор, Директор, Сотрудник).
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :param task_id: Уникальный идентификатор пользователя в телеграм.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """

    if usr_type == 'student':
        already_get = select_already_get_stud(task_id)
        if already_get:
            return student_task_already_choose
        return student_task_choose
    elif usr_type in ('admin', 'director') and have_task:
        return task_without_del
    elif usr_type == 'worker':
        return task_worker_ikb
    return task_ikb


def get_keyboard_more_task(usr_type, task_selected):
    """
    Функция получения клавиатуры в соответствии с типом пользователя при подробном просмотре задачи.
    :param usr_type: Тип пользователя
    :param task_selected: Просматриваемая задача
    :return: Клавиатура
    """

    if usr_type == 'student':
        return task_student_more_ikb
    if usr_type == 'worker':
        return task_worker_more_all
    if task_selected:
        return task_worker_more_without_del_ikb
    return task_worker_more_ikb


def get_tasks_for_student():
    """
    Функция получения списка задач для студентов
    :return: список задач для студентов
    """

    return [t for t in select_task() if not t.student_id or (len(t.student_id.split()) != int(t.num_people))]


def add_student_to_task(tasks, usr_id):
    """
    Функция для прикрепления студента к задаче
    """

    current_task = tasks[tasks_values[usr_id]]
    max_student_task = int(current_task.num_people)
    task_student_id = current_task.student_id

    if max_student_task == 1 or not task_student_id:
        change_task(current_task.task_id, 'student_id', usr_id)
    else:
        change_task(current_task.task_id, 'student_id', current_task.student_id + " " + usr_id)


@dp.callback_query_handler(text='show_task')
async def show_task(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = get_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=keyboard)
        await callback.answer()
        return

    if usr_id not in tasks_values:
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    count_tasks = len(tasks)
    student_ids_task = tasks[tasks_values[usr_id]].student_id
    keyboard = get_keyboard_task(u_type, student_ids_task, usr_id)

    page = tasks_values[usr_id]
    if tasks_values[usr_id] <= -1:
        page = count_tasks + tasks_values[usr_id]

    current_task = tasks[tasks_values[usr_id]]
    msg_text = f"<b>№</b> {page + 1}/{count_tasks}\n\n" + short_long_task(current_task)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text=['right', 'left'])
async def show_task_lr(callback: types.CallbackQuery):
    """
    Функция просмотра доступных пользователю задач.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    if not tasks:
        keyboard = get_keyboard(usr_id)
        msg_text = 'В данный момент задач нет.\nЗагляните позже.'
        await callback.message.edit_text(msg_text, reply_markup=keyboard)
        await callback.answer()
        return

    if usr_id not in tasks_values:
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    count_tasks = len(tasks)
    student_ids_task = tasks[tasks_values[usr_id]].student_id
    keyboard = get_keyboard_task(u_type, student_ids_task, usr_id)

    current_page = tasks_values[usr_id]
    s, tasks_values[usr_id] = navigation(callback.data, current_page, count_tasks)
    write_user_values("tasks_values", tasks_values)

    current_task = tasks[tasks_values[usr_id]]
    msg_text = s + short_long_task(current_task)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='more_task')
async def show_more_task(callback: types.CallbackQuery):
    """
    Функция просмотра подробной информации задачи.
    """

    usr_id = str(callback.from_user.id)
    u_type = user_type(usr_id)[0]

    if u_type == 'student':
        tasks = get_tasks_for_student()
    else:
        tasks = select_task()

    current_task = tasks[tasks_values[usr_id]]
    task_selected = current_task.student_id
    keyboard = get_keyboard_more_task(u_type, task_selected)
    msg_text = short_long_task(current_task, 1)

    await callback.message.edit_text(msg_text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)


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
    msg_text = (f"<b>Параметр:</b> {param_task.get(data['param'])}\n\n"
                f"<b>Новое значение:</b>\n{data['value']}\n\n")
    await message.answer(msg_text, parse_mode='HTML')

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

    await message.answer('Задача изменена.', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='del_task')
async def del_t(callback: types.CallbackQuery):
    """
    Функция для подтверждения действия удаления задачи.
    """

    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Удалить задачу?', reply_markup=del_task_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='del_yes', state=ConfirmDeletion.delete)
async def del_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция для удаления задачи.
    """

    await state.update_data(delete=callback.data)
    tasks = select_task()
    usr_id = str(callback.from_user.id)
    task_id = tasks[tasks_values[usr_id]].task_id
    count_tasks = len(tasks)
    del_task(task_id)

    wrong_page_1 = tasks_values[usr_id] >= count_tasks
    wrong_page_2 = tasks_values[usr_id] < count_tasks
    if count_tasks and (wrong_page_1 or wrong_page_2):
        tasks_values[usr_id] = 0
        write_user_values("tasks_values", tasks_values)

    await state.finish()
    await callback.message.edit_text('Задача удалена.', reply_markup=back_task_w_ikb)


@dp.callback_query_handler(text='stud_get_task')
async def stud_get_task(callback: types.CallbackQuery):
    """
    Функция для фиксирования выбора задачи студентом.
    """

    usr_id = str(callback.from_user.id)
    tasks = get_tasks_for_student()
    add_student_to_task(tasks, usr_id)

    task_name = select_already_get_stud(usr_id).task_name
    student_name = select_user(usr_id).name
    worker_id = tasks[tasks_values[usr_id]].from_id

    msg_text_worker = (f'Студент\ка <a href="tg://user?id={usr_id}">{student_name}</a> '
                       f'<b>выбрал\а</b> задачу <em>{task_name}</em>.')
    msg_text_student = (f'Задача <em>{task_name}</em> выбрана.\nВы можете отказаться '
                        f'от задачи, нажав в меню <em>Выбранная задача</em>.')

    await bot.send_message(worker_id, msg_text_worker, reply_markup=task_is_approve, parse_mode='HTML')
    await callback.message.edit_text(msg_text_student, parse_mode='HTML', reply_markup=back_task_ikb)
