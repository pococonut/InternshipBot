from sqlalchemy.exc import IntegrityError

from db.models.user import User, Student, Worker, Admin, Director, session


def registration_user(s_id, u_type, *args):
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
        who = True
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
