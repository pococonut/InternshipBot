from db.commands import user_type, select_user
from aiogram import types, Dispatcher
from keyboard import change_user_ikb

# ----------------- Отображение информации студента\работника -----------------


def print_stud(s):
    stud = f"<b>ФИО:</b> {s.student_name}\n\n" \
           f"<b>Номер телефона:</b> {s.phone}\n\n" \
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


def print_worker(w):
    worker = f"<b>ФИО:</b> {w.name}\n\n" \
             f"<b>Номер телефона:</b> {w.phone}\n\n" \
             f"<b>Дата регистрации:</b> {w.reg_date}\n"
    return worker


def show_inf(t_id):
    s_id = int(t_id)
    user_show = select_user(s_id)
    u_type = user_type(s_id)
    if u_type is None:
        inf = None
    else:
        if u_type[0] == 'student':
            inf = print_stud(user_show)
        else:
            inf = print_worker(user_show)
    return inf


async def show_params(message: types.Message):
    inf = show_inf(message.from_user.id)
    if inf is None:
        await message.answer('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.')
    else:
        await message.answer(f"🧑‍💻<b>Ваши данные</b>\n\n" + inf, parse_mode='HTML', reply_markup=change_user_ikb)


async def show_params_inline(callback: types.CallbackQuery):
    inf = show_inf(callback.from_user.id)
    if inf is None:
        await callback.message.edit_text('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.')
    else:
        await callback.message.edit_text(f"🧑‍💻<b>Ваши данные</b>\n\n" + inf, parse_mode='HTML', reply_markup=change_user_ikb)


def register_handlers_show(dp: Dispatcher):
    dp.register_message_handler(show_params, commands=['show'])
    dp.register_callback_query_handler(show_params_inline, text='show')