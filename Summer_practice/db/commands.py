import datetime
from db.models.user_add import AddedUser
from sqlalchemy.exc import IntegrityError
from db.models.applications import Application
from db.models.internship import Task, InternshipTask, Internship
from db.models.user import User, Student, Worker, Admin, Director, session


def registration_user(s_id, u_type, *args):
    """
    Функция записи данных нового пользователя в модель базы данных.
    :param s_id: Уникальный идентификатор пользователя в телеграм.
    :param u_type: Тип пользователя (Администратор, Директор, Сотрудник, Студент)
    :param args: Словарь с данными о пользователе.
    :return: Строка соответствующая с типом пользователя, при успешной записи. False при исключении.
    """
    user = None
    who = False
    if u_type == 'student':
        user = Student(telegram_id=str(s_id),
                       student_name=args[0]['student_name'],
                       name=args[0]['student_name'],
                       phone=args[0]['phone'],
                       university=args[0]['university'],
                       faculty=args[0]['faculty'],
                       specialties=args[0]['specialties'],
                       department=args[0]['department'],
                       course=args[0]['course'],
                       group=args[0]['group'],
                       coursework=args[0]['coursework'],
                       knowledge=args[0]['knowledge']
                       )
        who = 'student'
    elif u_type == 'admin':
        user = Admin(telegram_id=str(s_id),
                     admin_name=args[0]['name'],
                     name=args[0]['name'],
                     phone=args[0]['phone'],
                     login=args[0]['login'],
                     password=args[0]['password'],
                     )
        who = 'администратор'

    elif u_type == 'director':
        user = Director(telegram_id=str(s_id),
                        director_name=args[0]['name'],
                        name=args[0]['name'],
                        phone=args[0]['phone'],
                        login=args[0]['login'],
                        password=args[0]['password'],
                        )
        who = 'директор'

    elif u_type == 'worker':
        user = Worker(telegram_id=str(s_id),
                      worker_name=args[0]['name'],
                      name=args[0]['name'],
                      phone=args[0]['phone'],
                      login=args[0]['login'],
                      password=args[0]['password'],
                      )
        who = 'сотрудник'

    session.add(user)
    try:
        session.commit()
        return who
    except Exception as e:
        print(e)
        session.rollback()
        return False


def add_user(*args):
    """
    Функция добавления данных нового аккаунта в модель базы данных.
    :param args: Словарь с параметрами аккаунта.
    :return: True - при успешной записи, False - при исключении.
    """
    usr = AddedUser(
        login=args[0]['login'],
        password=args[0]['password'],
        type=args[0]['type'],
    )
    try:
        session.add(usr)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def add_task(f_id, *args):
    """
    Функция добавления данных задачи в модель базы данных.
    :param f_id: Уникальный идентификатор пользователя в телеграм, добавившего задачу.
    :param args: Словарь с параметрами задачи.
    :return: True - при успешной записи, False - при исключении.
    """
    task = Task(task_name=args[0]['task_name'],
                from_id=f_id,
                task_goal=args[0]['task_goal'],
                task_description=args[0]['task_description'],
                task_tasks=args[0]['task_tasks'],
                task_technologies=args[0]['task_technologies'],
                task_new_skills=args[0]['task_new_skills'],
                num_people=args[0]['num_people'],
                materials=args[0]['materials'])
    session.add(task)

    internship = Internship(beg_date='28-06-2023', end_date='28-07-2023')
    task.internship.append(internship)
    session.add(internship)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def add_application(stud_id, work_id, b):
    """
    Функция добавления результата рассмотрения заявки.
    :param stud_id: Уникальный идентификатор студента в телеграм.
    :param work_id: Уникальный идентификатор сотрудника в телеграм, принявшего решение.
    :param b: Булево значение, True - заявка одобрена, False - заявка отклонена.
    """
    application = Application(
        student_id=stud_id,
        worker_id=work_id,
        approve=b
    )
    session.add(application)
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # откатываем session.add(user)
        print(e)


def select_added_users():
    """
    Функция возвращающая все Добавленные аккаунты.
    :return: Список добавленных аккаунтов.
    """
    try:
        users = AddedUser.query.all()
    except Exception as e:
        print(e)
        users = False
    return users


def select_all_users():
    """
    Функция возвращающая всех Пользователей.
    :return: Список пользователей телеграм бота.
    """
    try:
        user = User.query.all()
    except Exception as e:
        print(e)
        user = False
    return user


def select_user(user_id):
    """
    Функция возвращающая информацию о пользователе с соответствующим id.
    :param user_id: Уникальный идентификатор пользователя в телеграм.
    :return: Информацию о пользователе.
    """
    try:
        user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        user = False
    return user


def select_task():
    """
    Функция возвращающая все добавленные задачи.
    :return: Список задач.
    """
    try:
        task = Task.query.order_by(Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_worker_task(f_id):
    """
    Функция возвращающая информацию о задачах, опубликованных пользователем с соответствующим id.
    :param f_id: Уникальный идентификатор пользователя в телеграм.
    :return: Список добавленных задач пользователя.
    """
    try:
        task = session.query(Task).filter(Task.from_id == str(f_id)).order_by(Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_task_for_stud():
    """
    Функция возвращающая невыбранные студентами задачи.
    :return: Список невыбранных задач.
    """
    try:
        task = session.query(Task).filter(Task.student_id == None).order_by(Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_already_get_stud(s_id):
    """
    Функция возвращающая задачу, выбранную студентом.
    :param s_id: Уникальный идентификатор студента в телеграм.
    :return: Задача, выбранная пользователем.
    """
    try:
        task = session.query(Task).filter(Task.student_id != None).order_by(Task.task_id.desc()).all()
        for t in task:
            if str(s_id) in t.student_id:
                task = t
                break
            else:
                task = False
    except Exception as e:
        print(e)
        task = False
    print(task)

    return task


def select_chosen_tasks(w_id):
    """
    Функция возвращающая задачи, которые были выбраны студентами.
    :param w_id: Уникальный идентификатор сотрудника в телеграм.
    :return: Список задач, которые были выбраны студентами.
    """
    try:
        task = session.query(Task).filter(Task.student_id != None, Task.from_id == str(w_id)).order_by(
            Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_students():
    """
    Функция выбора всех студентов, оставивших заявки.
    :return: Список студентов.
    """
    try:
        students = Student.query.order_by(User.reg_date.desc()).all()
    except Exception as e:
        print(e)
        students = False
    return students


def select_applications():
    """
    Функция возвращающая результаты рассмотрения заявок.
    :return: Список результатов рассмотрения заявок.
    """
    try:
        applications = Application.query.all()
    except Exception as e:
        print(e)
        applications = False
    return applications


def change_task(t_id, column, new_val):
    """
    Функция изменения параметра задачи на новое значение.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :param column: Название столбца модели базы данных.
    :param new_val: Новое значение.
    """
    session.query(Task).filter(Task.task_id == str(t_id)).update({f'{column}': new_val})
    session.commit()


def change_task_stud(s_id, column, new_val):
    """
    Функция отказа студента от задачи.
    :param s_id: Уникальный идентификатор пользователя в телеграм.
    :param column: Столбец модели базы данных, отвечающий за сохранение id пользователя, выбравшего задачу.
    :param new_val: Новое значение - None.
    """
    s_id = str(s_id)
    task = session.query(Task).filter(Task.student_id != None).order_by(Task.task_id.desc()).all()
    for t in task:
        if t.student_id == s_id:
            session.query(Task).filter(Task.student_id == s_id).update({f'{column}': new_val})
            break
        else:
            if len(t.student_id.split()) > 1 and s_id in t.student_id:
                new_s_id = " ".join(t.student_id.replace(s_id, '').strip(' ').split())
                print(new_s_id)
                session.query(Task).filter(Task.task_id == t.task_id).update({f'{column}': new_s_id})

    session.commit()


def change_name_added(login, new_val):
    """
    Функция записи ФИО пользователя при верной авторизации, в соответствующем аккаунте.
    :param login: Логин аккаунта.
    :param new_val: Пароль аккаунта.
    """
    session.query(AddedUser).filter(AddedUser.login == str(login)).update({f'name_usr': new_val})
    session.commit()


def change_inform(t_id, u_type, column, new_val):
    """
    Функция изменения данных пользователя.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :param u_type: Тип пользователя (Администратор, Директор, Сотрудник, Студент)
    :param column: Название столбца.
    :param new_val: Новое значение.
    """
    if column in User.__table__.columns:
        session.query(User).filter(User.telegram_id == str(t_id)).update({f'{column}': new_val})
    else:
        if u_type == 'student':
            session.query(Student).filter(Student.telegram_id == str(t_id)).update({f'{column}': new_val})
        else:
            session.query(User).filter(User.telegram_id == str(t_id)).update({f'name': new_val})

            if u_type == 'admin':
                session.query(Admin).filter(Admin.telegram_id == str(t_id)).update({f'admin_name': new_val})
            elif u_type == 'worker':
                session.query(Worker).filter(Worker.telegram_id == str(t_id)).update({f'worker_name': new_val})
            elif u_type == 'director':
                session.query(Director).filter(Director.telegram_id == str(t_id)).update({f'director_name': new_val})

    session.query(User).filter(User.telegram_id == str(t_id)).update({'upd_date': datetime.date.today()})
    session.commit()


def del_task(t_id):
    """
    Функция удаления задачи
    :param t_id: Уникальный идентификатор задачи.
    """
    try:
        x1 = session.query(InternshipTask).filter(InternshipTask.task_id == str(t_id)).one()
        session.delete(x1)
        session.commit()

        x2 = session.query(Task).filter(Task.task_id == str(t_id)).one()
        session.delete(x2)
        session.commit()

        x3 = session.query(Internship).filter(Internship.internship_id == str(t_id)).one()
        session.delete(x3)
        session.commit()

    except Exception as e:
        print(e)


def del_added(a_id):
    """
    Функция удаления добавленного аккаунта.
    :param a_id: Уникальный идентификатор аккаунта.
    :return:
    """
    try:
        x1 = session.query(AddedUser).filter(AddedUser.id == str(a_id)).one()
        session.delete(x1)
        session.commit()
    except Exception as e:
        print(e)


def user_type(user_id):
    """
    Функция возвращающая тип пользователя (Администратор, Директор, Сотрудник, Студент).
    :param user_id: Уникальный идентификатор пользователя.
    :return: Тип пользователя.
    """
    try:
        u_type = session.query(User.type).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        u_type = False
    return u_type


def stud_approve(s_id):
    """
    Функция возвращающая результат рассмотрения заявки студента.
    :param s_id: Уникальный идентификатор студента.
    :return: Результат рассмотрения заявки.
    """
    try:
        approve = session.query(Application.approve).filter(Application.student_id == str(s_id)).first()
    except Exception as e:
        print(e)
        approve = False
    return approve

