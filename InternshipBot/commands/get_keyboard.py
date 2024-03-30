from keyboard import *
from db.commands import get_user_type, select_already_get_stud, stud_approve, select_user


def get_account_keyboard(t_id):
    """
    Функция возвращающая соответствующую inline-клавиатуру в зависимости от типа пользователя.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :return k: Inline-клавиатура.
    """

    u_type = get_user_type(t_id)
    if not u_type:
        return back_ikb
    if u_type[0] in ('admin', 'director'):
        return admin_ikb
    if u_type[0] == 'worker':
        return worker_ikb
    if u_type[0] == 'student':
        approve = stud_approve(t_id)
        if approve:
            return stud_is_approve
        return student_not_approved


def change_keyboard(task_id):
    """
    Функция возвращающая клавиатуру с параметрами доступными для изменения в зависимости от типа пользователя.
    :param task_id: Уникальный идентификатор пользователя в телеграм.
    :return k: Inline-клавиатура.
    """

    user_exist = select_user(task_id)
    if not user_exist:
        return None

    u_type = get_user_type(task_id)
    if u_type[0] == 'student':
        return change_ikb
    return change_worker_ikb


def get_keyboard_deletion(callback):
    """
    Функция для получения клавиатуры при удалении задачи
    :param callback: Кнопка
    :return: Клавиатура
    """

    if 'worker' in callback:
        return del_task_worker_ikb
    return del_task_ikb


def get_keyboard_task(callback, usr_id, have_task):
    """
    Функция получения клавиатуры в соответствии с типом пользователя.
    :param callback: Кнопка.
    :param usr_id: Идентификатор пользователя.
    :param have_task: Параметр, указывающий на наличие у студента выбранной задачи.
    :return: Клавиатура пользователя, в зависимости от его типа.
    """

    if 'worker' in callback:
        if have_task:
            return task_worker_without_del
        return task_worker_own_ikb

    usr_type = get_user_type(usr_id)[0]
    if usr_type == 'student':
        already_get = select_already_get_stud(usr_id)
        if already_get:
            return student_task_already_choose
        return student_task_choose
    elif usr_type in ('admin', 'director') and have_task:
        return task_without_del
    elif usr_type == 'worker':
        return task_worker_ikb
    return task_ikb


def get_keyboard_more_task(usr_id, task_selected, callback):
    """
    Функция получения клавиатуры в соответствии с типом пользователя при подробном просмотре задачи.
    :param usr_id: Идентификатор пользователя
    :param task_selected: Просматриваемая задача
    :param callback: Кнопка
    :return: Клавиатура
    """

    if callback == "more_task_student_chosen":
        return stud_more_task
    if 'worker' in callback:
        if task_selected:
            return task_worker_more_without_del_w_ikb
        return task_worker_more_w_ikb

    user_type = get_user_type(usr_id)[0]
    if user_type == 'student':
        return task_student_more_ikb
    if user_type == 'worker':
        return task_worker_more_all
    if task_selected:
        return task_worker_more_without_del_ikb
    return task_worker_more_ikb

