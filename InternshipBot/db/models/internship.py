import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, VARCHAR, TEXT, DATE, Integer, String, ForeignKey, PrimaryKeyConstraint

from db.models.user import Base


class Task(Base):
    """Модель таблицы задач.
        :task_id: Уникальный идентификатор таблицы.
        :from_id: Идентификатор сотрудника, опубликовавшего задачу.
        :student_id: Идентификатор студента, выбравшего задачу.
        :task_name: Название задачи.
        :task_goal: Цель задачи.
        :task_description: Описание задачи.
        :task_tasks: Поставленные подзадачи.
        :task_technologies: Навыки и технологии, необходимые для реализации задачи.
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
    internship_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    beg_date = Column(DATE, default=datetime.date.today())
    end_date = Column(DATE, default=datetime.date.today())

    task = relationship("Task", secondary='internship_task', overlaps="internship")


class InternshipTask(Base):
    """Модель промежуточной таблицы, связывающей стажировки и задачи.
        :task_id: Уникальный идентификатор задачи.
        :internship_id: Уникальный идентификатор стажировки.
    """

    __tablename__ = "internship_task"
    __table_args__ = (PrimaryKeyConstraint('task_id', 'internship_id'),)

    task_id = Column(Integer, ForeignKey('task.task_id'))
    internship_id = Column(Integer, ForeignKey('internship.internship_id'))


