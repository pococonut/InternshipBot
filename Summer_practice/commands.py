from sqlalchemy.exc import PendingRollbackError, IntegrityError

from db.student import session, Student
from db.user import User, Student_2, Worker, Admin, Director
from db.text import Text
from db.internship import Task, InternshipTask, Internship


def register_student(s_id, *args):
    student = Student_2(telegram_id=str(s_id),
                        student_name=args[0]['student_name'],
                        name=args[0]['student_name'],
                        university=args[0]['university'],
                        faculty=args[0]['faculty'],
                        specialties=args[0]['specialties'],
                        department=args[0]['department'],
                        course=args[0]['course'],
                        group=args[0]['group'],
                        coursework=args[0]['coursework'],
                        knowledge=args[0]['knowledge']
                        )

    session.add(student)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def register_admin(s_id, *args):
    admin = Admin(telegram_id=str(s_id),
                  admin_name=args[0]['name'],
                  name=args[0]['name'],
                  login=args[0]['login'],
                  password=args[0]['password'],
                  )

    session.add(admin)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def add_task(*args):
    task = Task(task_name=args[0]['task_name'],
                task_description=args[0]['task_description'],
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
        session.rollback()  # откатываем session.add(user)
        return False


def add_internship_task(*args):
    internship_task = InternshipTask(
                      task_name=args[0]['task_name'],
                      task_description=args[0]['task_description'],
                      num_people=args[0]['num_people'],
                      materials=args[0]['materials'],
                    )
    session.add(internship_task)


    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def get_txt(txt):
    m = Text(message=txt)

    session.add(m)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def select_txt():
    try:
        m = session.query(Text.message).all()
    except Exception as e:
        print(e)
        m = False
    return m


def delete_txt():
    try:
        session.query(Text).delete()
        session.commit()
    except Exception as e:
        print(e)


def select_user(user_id):
    try:
        user = session.query(User).filter(User.telegram_id == str(user_id)).first()
        user_type = session.query(User.type).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        user = False
    return user


def user_type(user_id):
    try:
        user_type = session.query(User.type).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        user_type = False
    return user_type


def select_employee(user_id):
    try:
        a_n = session.query(Admin.admin_name).filter(Admin.telegram_id == str(user_id)).first()
        a_log = session.query(Admin.login).filter(Admin.telegram_id == str(user_id)).first()
        a_pass = session.query(Admin.password).filter(Admin.telegram_id == str(user_id)).first()
        adm_authorisation = [a_n, a_log, a_pass]
    except Exception as e:
        print(e)
        adm_authorisation = False
    return adm_authorisation


def change_stud_inform(s_id, column, new_val):
    session.query(Student_2).filter(Student_2.telegram_id == str(s_id)).update({f'{column}': new_val})
    session.commit()
