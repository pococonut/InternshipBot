from db.commands import user_type, stud_approve
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard import back_ikb, admin_ikb, worker_ikb, ikb_3, stud_is_approve


class ConfirmDeletion(StatesGroup):
    delete = State()


def get_keyboard(t_id):
    """
    Функция возвращающая соответствующую inline-клавиатуру в зависимости от типа пользователя.

    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :return k: Inline-клавиатура.
    """
    u_type = user_type(t_id)
    if u_type is None:
        k = back_ikb
    else:
        if u_type[0] in ('admin', 'director'):
            k = admin_ikb
        elif u_type[0] == 'worker':
            k = worker_ikb
        elif u_type[0] == 'student':
            approve = stud_approve(t_id)
            k = ikb_3
            if approve:
                k = stud_is_approve
    return k


def print_stud(s, c=None):
    """
    Функция возвращающая данные студента в виде строки.
    :param s:  Строка модели БД, относящаяся к конкретному студенту, с информацией о нем.
    :param c:  Кнопка.
    :return: Строка с данными студента.
    """
    if c is None:
        stud = f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n\n"
    else:
        stud = f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n\n"
    stud += f"<b>Номер телефона:</b> <code>{s.phone}</code>\n\n"\
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