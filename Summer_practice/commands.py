from sqlalchemy.exc import PendingRollbackError, IntegrityError

from db.student import session, Student


def register_student(s_id, student_name, university, faculty, specialties, department, course, group, coursework,knowledge):
    student = Student(student_id=s_id,
                      student_name=student_name,
                      university=university,
                      faculty=faculty,
                      specialties=specialties,
                      department=department,
                      course=course,
                      group=group,
                      coursework=coursework,
                      knowledge=knowledge
                      )

    session.add(student)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False