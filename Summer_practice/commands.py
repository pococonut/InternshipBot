from sqlalchemy.exc import PendingRollbackError, IntegrityError

from db.student import session, Student
from db.text import Text


def register_student(s_id=0, *args):
    student = Student(student_id=s_id,
                      student_name=args[0]['student_name'],
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


def select_student(user_id):
    try:
        student = session.query(Student).filter(Student.student_id == user_id).first()
    except Exception as e:
        print(e)
        student = False
    return student


def change_stud_inform(s_id, column, new_val):
    session.query(Student).filter(Student.student_id == s_id).update({f'{column}': new_val})
    session.commit()