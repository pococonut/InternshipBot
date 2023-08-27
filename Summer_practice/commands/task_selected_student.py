from aiogram import types
from create import bot, dp
from aiogram.dispatcher import FSMContext
from commands.general import ConfirmDeletion
from commands.task_actions import short_long_task
from keyboard import stud_is_approve, stud_reject_task, reject_task_ikb, task_is_approve
from db.commands import select_already_get_stud, change_task_stud, select_user


@dp.callback_query_handler(text='stud_chosen_tasks')
async def stud_chosen_task(callback: types.CallbackQuery):
    """
    Функция просмотра выбранной студентом задачи.
    """
    try:
        task = select_already_get_stud(callback.from_user.id)
        print(task)
        if not task:
            await callback.message.edit_text('Вы еще не выбрали задачу.', reply_markup=stud_is_approve)
            await callback.answer()
        else:
            await callback.message.edit_text(f"📝 <b>Выбранная задача</b>\n\n" + short_long_task(task, 1),
                                             parse_mode='HTML', reply_markup=stud_reject_task,
                                             disable_web_page_preview=True)
    except Exception as e:
        print(e)


@dp.callback_query_handler(text='reject_task')
async def stud_reject_t(callback: types.CallbackQuery):
    """
    Функция подтверждения отказа от задачи.
    """
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Отказаться от задачи?', parse_mode='HTML', reply_markup=reject_task_ikb)
    await ConfirmDeletion.delete.set()


@dp.callback_query_handler(text='reject_task_yes', state=ConfirmDeletion.delete)
async def stud_reject_t_yes(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция отказа от задачи.
    """
    print('!!!!!!!!')
    await state.update_data(delete=callback.data)
    worker_id = select_already_get_stud(callback.from_user.id).from_id
    task_name = select_already_get_stud(callback.from_user.id).task_name
    change_task_stud(callback.from_user.id, 'student_id', None)
    student_name = select_user(callback.from_user.id).name
    await bot.send_message(worker_id, f'Студент\ка <a href="tg://user?id={callback.from_user.id}">{student_name}</a> '
                                      f'<b>отказался\ась</b> от задачи <em>{task_name}</em>.',
                           reply_markup=task_is_approve, parse_mode='HTML')

    await callback.message.edit_text('Вы отказались от выбранной задачи.', reply_markup=stud_is_approve)
    await state.finish()