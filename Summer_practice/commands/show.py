from db.commands import user_type, select_user
from aiogram import types, Dispatcher
from keyboard import change_stud_ikb

# ----------------- Отображение информации студента\работника -----------------


def print_stud(s):
    stud = f"<b>ФИО:</b> {s.student_name}\n\n" \
           f"<b>ВУЗ:</b> {s.university}\n\n" \
           f"<b>Факультет:</b> {s.faculty}\n\n" \
           f"<b>Специальность:</b> {s.specialties}\n\n" \
           f"<b>Кафедра:</b> {s.department}\n\n" \
           f"<b>Курс:</b> {s.course}\n\n" \
           f"<b>Группа:</b> {s.group}\n\n" \
           f"<b>Курсовые:</b> {s.coursework}\n\n" \
           f"<b>Знания:</b> {s.knowledge}\n\n" \
           f"<b>Дата регистрации:</b> {s.reg_date}\n"
    return stud


async def show_params(message: types.Message):
    s_id = int(message.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                             parse_mode='HTML')
    elif u_type[0] == 'student':
        await message.answer(f"🧑‍💻<b>Ваши данные</b>\n\n" + print_stud(user_show), parse_mode='HTML',
                             reply_markup=change_stud_ikb)
    else:
        await message.answer(f"🧑‍💻<b>Ваши данные</b>\n\n<b>ФИО:</b> {user_show.name}\n\n", parse_mode='HTML')


async def show_params_inline(callback: types.CallbackQuery):
    s_id = int(callback.from_user.id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        await callback.message.edit_text('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                         parse_mode='HTML')
    elif u_type[0] == 'student':
        await callback.message.edit_text(f"🧑‍💻<b>Ваши данные</b>\n\n" + print_stud(user_show), parse_mode='HTML',
                                         reply_markup=change_stud_ikb)
    else:
        await callback.message.edit_text(f"🧑‍💻<b>Ваши данные</b>\n\n<b>ФИО:</b> {user_show.name}\n\n", parse_mode='HTML')


def register_handlers_show(dp: Dispatcher):
    dp.register_message_handler(show_params, commands=['show'])
    dp.register_callback_query_handler(show_params_inline, text='show')