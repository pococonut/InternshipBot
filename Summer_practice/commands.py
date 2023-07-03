from sqlalchemy.exc import PendingRollbackError, IntegrityError

from db.student import session, Student


def register_student(s_id=0, *args):
    student = Student(student_id=s_id,
                      student_name=args[0][0],
                      university=args[0][1],
                      faculty=args[0][2],
                      specialties=args[0][3],
                      department=args[0][4],
                      course=args[0][5],
                      group=args[0][6],
                      coursework=args[0][7],
                      knowledge=args[0][8]
                      )

    session.add(student)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def select_student(user_id):
    try:
        student = session.query(Student).filter(Student.student_id == user_id).first()
    except Exception as e:
        print(e)
        student = False
    return student
