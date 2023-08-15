import os
from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, Integer, Boolean, String, ForeignKey, \
    PrimaryKeyConstraint
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker, relationship
import datetime
from config import settings

load_dotenv()

host = settings.host
password = settings.password
database = settings.database

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Task(Base):
    """Модель таблицы задач.

        :task_id: Уникальный идентификатор таблицы.

        :from_id: Идентификатор сотрудника, опубликовавшего задачу.
        :student_id: Идентификатор студента, выбравшего задачу.

        :task_name: Название задачи.
        :task_goal: Цель задачи.
        :task_description: Описание задачи.
        :task_tasks: Поставленные подзадачи.
        :task_technologies: Необходимые навыки и технологии для реализации задачи.
        :task_new_skills: Навыки, приобретаемые в процессе прохождения практики.
        :num_people: Количество людей.
        :materials: Материалы.
    """

    __tablename__ = "task"

    task_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)

    from_id = Column(String, nullable=True)

    student_id = Column(String, nullable=True)

    task_name = Column(VARCHAR(200))

    task_goal = Column(TEXT)

    task_description = Column(TEXT)

    task_tasks = Column(TEXT)

    task_technologies = Column(TEXT)

    task_new_skills = Column(TEXT)

    num_people = Column(VARCHAR(10))

    materials = Column(TEXT)

    internship = relationship("Internship", secondary='internship_task')


class Internship(Base):
    """Модель таблицы стажировок.

        :internship_id: Уникальный идентификатор стажировки.

        :beg_date: Дата начала стажировки.
        :end_date: Дата окончания стажировки.
    """
    __tablename__ = "internship"

    # telegram user id
    internship_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # ФИО
    beg_date = Column(DATE, default=datetime.date.today())
    # last update date
    end_date = Column(DATE, default=datetime.date.today())

    task = relationship("Task", secondary='internship_task', overlaps="internship")


class InternshipTask(Base):
    """Модель промежуточной таблицы стажировок и задач.

        :task_id: Уникальный идентификатор задачи.
        :internship_id: Уникальный идентификатор стажировки.
    """

    __tablename__ = "internship_task"

    __table_args__ = (PrimaryKeyConstraint('task_id', 'internship_id'),)

    task_id = Column(Integer, ForeignKey('task.task_id'))

    internship_id = Column(Integer, ForeignKey('internship.internship_id'))


Base.metadata.create_all(bind=engine)


#InternshipTask.__table__.drop(engine)

#session.query(Task).filter(Task.student_id != None).update({f'student_id': None})
#session.commit()

