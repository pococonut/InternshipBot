import os
from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, Integer, Boolean, String, ForeignKey, \
    PrimaryKeyConstraint
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker, relationship
import datetime
load_dotenv()

host = "localhost"
password = "123"
database = "bot"

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Task(Base):
    __tablename__ = "task"

    # telegram user id
    task_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # ФИО
    from_id = Column(String, nullable=True)

    student_id = Column(String, nullable=True)

    task_name = Column(VARCHAR(200))

    task_description = Column(TEXT)

    num_people = Column(VARCHAR(10))

    materials = Column(TEXT, nullable=True)

    internship = relationship("Internship", secondary='internship_task')


class Internship(Base):
    __tablename__ = "internship"

    # telegram user id
    internship_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # ФИО
    beg_date = Column(DATE, default=datetime.date.today())
    # last update date
    end_date = Column(DATE, default=datetime.date.today())

    task = relationship("Task", secondary='internship_task')


class InternshipTask(Base):
    __tablename__ = "internship_task"

    __table_args__ = (PrimaryKeyConstraint('task_id', 'internship_id'),)

    #id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)

    task_id = Column(Integer, ForeignKey('task.task_id'))

    internship_id = Column(Integer, ForeignKey('internship.internship_id'))


#InternshipTask.__table__.drop(engine)

Base.metadata.create_all(bind=engine)

#session.query(Task).filter(Task.student_id != None).update({f'student_id': None})
#session.commit()

"""task = Task(task_name='x', task_description='x', num_people='1', materials='x')
session.add(task)

internship = Internship(beg_date='28-06-2023', end_date='28-07-2023')
task.internship.append(internship)
session.add(internship)"""

#internship = Internship(beg_date='2023-06-28', end_date='2023-07-28')
#session.add(internship)
#session.commit()
