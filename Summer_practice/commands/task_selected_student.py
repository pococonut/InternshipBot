from commands.back import back_func
from commands.task_actions import short_long_task
from db.commands import select_already_get_stud, select_worker_reject, change_task_stud, select_user
from keyboard import stud_is_approve, stud_reject_task, reject_task_ikb, task_is_approve
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create import bot


# ----------------- Просмотр выбранной студентом задачи (для студента) -----------------


async def stud_chosen_task(callback: types.CallbackQuery):
    try:
        task = select_already_get_stud(callback.from_user.id)
        if not task:
            await callback.message.edit_text('Вы еще не выбрали задачу.', reply_markup=stud_is_approve)
        else:
            await callback.message.edit_text(f"📝 <b>Выбранная задача</b>\n\n" + short_long_task(task, 1),
                                             parse_mode='HTML', reply_markup=stud_reject_task,
                                             disable_web_page_preview=True)
    except Exception as e:
        print(e)


# ----------------- Отказ от выбранной студентом задачи -----------------


class RejectTaskStud(StatesGroup):
    reject_ts = State()


async def stud_reject_t(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Отказаться от задачи?', parse_mode='HTML', reply_markup=reject_task_ikb)
    await RejectTaskStud.reject_ts.set()


async def reject_task_yes(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(reject_task=callback.data)

    worker_id = select_worker_reject(callback.from_user.id).from_id
    task_name = select_worker_reject(callback.from_user.id).task_name
    change_task_stud(callback.from_user.id, 'student_id', None)
    student_name = select_user(callback.from_user.id).name
    await bot.send_message(worker_id, f'Студент\ка <a href="tg://user?id={callback.from_user.id}">{student_name}</a> '
                                      f'<b>отказался\ась</b> от задачи <em>{task_name}</em>.',
                           reply_markup=task_is_approve, parse_mode='HTML')

    await callback.message.edit_text('Вы отказалить от выбранной задачи.', reply_markup=stud_is_approve)
    await state.finish()


def register_handlers_task_selected_student(dp: Dispatcher):
    dp.register_callback_query_handler(stud_chosen_task, text='stud_chosen_tasks')
    dp.register_callback_query_handler(stud_reject_t, text='reject_task')
    dp.register_callback_query_handler(reject_task_yes, text='reg_task_yes', state=RejectTaskStud.reject_ts)
    dp.register_callback_query_handler(back_func, text='back', state="*")