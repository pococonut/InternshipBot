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


class Application(Base):
    __tablename__ = "application"

    # telegram user id
    application_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # ФИО
    student_id = Column(String, unique=True)

    worker_id = Column(String)

    approve = Column(Boolean)


Base.metadata.create_all(bind=engine)

"""task = Task(task_name='x', task_description='x', num_people='1', materials='x')
session.add(task)

internship = Internship(beg_date='28-06-2023', end_date='28-07-2023')
task.internship.append(internship)
session.add(internship)"""

#internship = Internship(beg_date='2023-06-28', end_date='2023-07-28')
#session.add(internship)
#session.commit()
