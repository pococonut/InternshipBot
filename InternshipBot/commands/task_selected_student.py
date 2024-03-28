from aiogram import types
from aiogram.dispatcher import FSMContext
from create import bot, dp
from commands.task_actions import tasks_values
from commands.get_menu import callback_check_authentication
from commands.general import ConfirmDeletion, get_tasks_for_student, short_long_task
from db.commands import select_already_get_stud, change_task_stud, select_user, change_task
from keyboard import stud_is_approve, stud_reject_task, reject_task_ikb, task_is_approve, back_task_ikb


def add_student_to_task(tasks, usr_id):
    """
    Функция для фиксирования задачи за студентом
    :param tasks: Список задач
    :param usr_id: Идентификатор пользователя
    :return: None
    """

    current_task = tasks[tasks_values[usr_id]]
    max_student_task = int(current_task.num_people)
    task_student_id = current_task.student_id

    if max_student_task == 1 or not task_student_id:
        change_task(current_task.task_id, 'student_id', usr_id)
        return
    lst_students_ids = current_task.student_id + " " + usr_id
    change_task(current_task.task_id, 'student_id', lst_students_ids)


@dp.callback_query_handler(text='stud_get_task')
@callback_check_authentication
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


@dp.callback_query_handler(text='stud_chosen_tasks')
@callback_check_authentication
async def stud_chosen_task(callback: types.CallbackQuery):
    """
    Функция просмотра выбранной студентом задачи.
    """

    task = select_already_get_stud(callback.from_user.id)
    if not task:
        await callback.message.edit_text('Вы еще не выбрали задачу.', reply_markup=stud_is_approve)
        await callback.answer()
        return

    m = f"📝 <b>Выбранная задача</b>\n\n" + short_long_task(task, 0)
    await callback.message.edit_text(m, parse_mode='HTML', reply_markup=stud_reject_task, disable_web_page_preview=True)


@dp.callback_query_handler(text='reject_task')
@callback_check_authentication
async def stud_reject_t(callback: types.CallbackQuery):
    """
    Функция подтверждения отказа от задачи.
    """

    msg_text = 'Отказаться от задачи?'
    await callback.message.edit_text(msg_text, reply_markup=reject_task_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='reject_task_yes', state=ConfirmDeletion.delete)
@callback_check_authentication
async def stud_reject_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция отказа от задачи.
    """

    await state.update_data(delete=callback.data)
    worker_id = select_already_get_stud(callback.from_user.id).from_id
    task_name = select_already_get_stud(callback.from_user.id).task_name
    change_task_stud(callback.from_user.id, 'student_id', None)
    student_name = select_user(callback.from_user.id).name

    msg_text_worker = f'Студент\ка <a href="tg://user?id={callback.from_user.id}">{student_name}</a> ' \
                      f'<b>отказался\ась</b> от задачи <em>{task_name}</em>.'
    msg_text_student = 'Вы отказались от выбранной задачи.'

    await bot.send_message(worker_id, msg_text_worker, reply_markup=task_is_approve, parse_mode='HTML')
    await callback.message.edit_text(msg_text_student, reply_markup=stud_is_approve)
    await state.finish()