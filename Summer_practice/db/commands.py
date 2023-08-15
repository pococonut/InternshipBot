from sqlalchemy.exc import IntegrityError
from db.models.user import User, Student, Worker, Admin, Director, session
from db.models.internship import Task, InternshipTask, Internship
from db.models.applications import Application
import datetime

from db.models.user_add import AddedUser


def register_student(s_id, *args):
    student = Student(telegram_id=str(s_id),
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
                  phone=args[0]['phone'],
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


def register_director(s_id, *args):
    director = Director(telegram_id=str(s_id),
                        director_name=args[0]['name'],
                        name=args[0]['name'],
                        phone=args[0]['phone'],
                        login=args[0]['login'],
                        password=args[0]['password'],
                        )
    session.add(director)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_worker(s_id, *args):
    worker = Worker(telegram_id=str(s_id),
                    worker_name=args[0]['name'],
                    name=args[0]['name'],
                    phone=args[0]['phone'],
                    login=args[0]['login'],
                    password=args[0]['password'],
                    )
    session.add(worker)
    try:
        session.commit()
        return True
    except Exception as e:
        print(e)
        session.rollback()
        return False


def add_user(*args):
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


def add_application(stud_id, work_id, b):
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
    try:
        users = AddedUser.query.all()
    except Exception as e:
        print(e)
        users = False
    return users


def select_all_users():
    try:
        user = User.query.all()
    except Exception as e:
        print(e)
        user = False
    return user


def select_user(user_id):
    try:
        user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        user = False
    return user


def select_task():
    try:
        task = Task.query.order_by(Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_worker_task(f_id):
    try:
        task = session.query(Task).filter(Task.from_id == str(f_id)).order_by(Task.task_id.desc()).all()
        # user_type = session.query(User.type).filter(User.telegram_id == str(user_id)).first()

    except Exception as e:
        print(e)
        task = False
    return task


def select_task_for_stud():
    try:
        task = session.query(Task).filter(Task.student_id == None).order_by(Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_already_get_stud(s_id):
    try:
        task = session.query(Task).filter(Task.student_id == str(s_id)).order_by(Task.task_id.desc()).first()
    except Exception as e:
        print(e)
        task = False
    return task


def select_worker_reject(s_id):
    try:
        task = session.query(Task).filter(Task.student_id == str(s_id)).order_by(Task.task_id.desc()).first()
    except Exception as e:
        print(e)
        task = False
    return task


def select_chosen_tasks(w_id):
    try:
        task = session.query(Task).filter(Task.student_id != None, Task.from_id == str(w_id)).order_by(
            Task.task_id.desc()).all()
    except Exception as e:
        print(e)
        task = False
    return task


def select_students():
    try:
        students = Student.query.order_by(User.reg_date.desc()).all()
    except Exception as e:
        print(e)
        students = False
    return students


def select_applications():
    try:
        applications = Application.query.all()
    except Exception as e:
        print(e)
        applications = False
    return applications


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


def change_task(t_id, column, new_val):
    session.query(Task).filter(Task.task_id == str(t_id)).update({f'{column}': new_val})
    session.commit()


def change_task_stud(s_id, column, new_val):
    session.query(Task).filter(Task.student_id == str(s_id)).update({f'{column}': new_val})
    session.commit()


def change_name_added(login, new_val):
    session.query(AddedUser).filter(AddedUser.login == str(login)).update({f'name_usr': new_val})
    session.commit()


def change_inform(id, type, column, new_val):
    if column in User.__table__.columns:
        session.query(User).filter(User.telegram_id == str(id)).update({f'{column}': new_val})
    else:
        if type == 'student':
            session.query(Student).filter(Student.telegram_id == str(id)).update({f'{column}': new_val})
        else:
            session.query(User).filter(User.telegram_id == str(id)).update({f'name': new_val})

            if type == 'admin':
                session.query(Admin).filter(Admin.telegram_id == str(id)).update({f'admin_name': new_val})
            elif type == 'worker':
                session.query(Worker).filter(Worker.telegram_id == str(id)).update({f'worker_name': new_val})
            elif type == 'director':
                session.query(Director).filter(Director.telegram_id == str(id)).update({f'director_name': new_val})

    session.query(User).filter(User.telegram_id == str(id)).update({'upd_date': datetime.date.today()})
    session.commit()


def del_task(t_id):
    try:
        x1 = session.query(InternshipTask).filter(InternshipTask.task_id == t_id).one()
        session.delete(x1)
        session.commit()

        x2 = session.query(Task).filter(Task.task_id == t_id).one()
        session.delete(x2)
        session.commit()

        x3 = session.query(Internship).filter(Internship.internship_id == t_id).one()
        session.delete(x3)
        session.commit()

    except Exception as e:
        print(e)


def del_added(a_id):
    try:
        x1 = session.query(AddedUser).filter(AddedUser.id == a_id).one()
        session.delete(x1)
        session.commit()
    except Exception as e:
        print(e)


def user_type(user_id):
    try:
        u_type = session.query(User.type).filter(User.telegram_id == str(user_id)).first()
    except Exception as e:
        print(e)
        u_type = False
    return u_type


def stud_approve(s_id):
    try:
        approve = session.query(Application.approve).filter(Application.student_id == str(s_id)).first()
    except Exception as e:
        print(e)
        approve = False
    return approve

