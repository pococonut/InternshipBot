import os
from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, Integer, Boolean, String, ForeignKey
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
import datetime
load_dotenv()

host = "localhost"
password = "123"
database = "bot"

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = "user"

    # telegram user id
    telegram_id = Column(String, unique=True,  nullable=False, primary_key=True, )
    # ФИО
    type = Column(VARCHAR(50), nullable=False)
    # ВУЗ
    name = Column(VARCHAR(50), nullable=False)

    reg_date = Column(DATE, default=datetime.date.today())
    # last update date
    upd_date = Column(DATE, onupdate=datetime.date.today())

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }


class Student_2(User):
    __tablename__ = "student_2"
    telegram_id = Column(String, ForeignKey(User.telegram_id), primary_key=True)

    student_name = Column(VARCHAR(50), nullable=False)
    # ВУЗ
    university = Column(VARCHAR(100), nullable=False)
    # факультет
    faculty = Column(VARCHAR(100), nullable=False)
    # направление
    specialties = Column(VARCHAR(100), nullable=False)
    # кафедра
    department = Column(VARCHAR(100), nullable=True)
    # курс
    course = Column(VARCHAR(10), nullable=False)
    # группа
    group = Column(VARCHAR(10), nullable=False)
    # темы курсовых работ
    coursework = Column(TEXT, nullable=True)
    # знания
    knowledge = Column(TEXT, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Worker(User):
    __tablename__ = "worker"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    worker_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "worker",
    }


Base.metadata.create_all(bind=engine)
"""
try:
    student1 = Student_2(telegram_id='9',
                         student_name='x',
                         name='x',
                         university="x",
                         faculty="x",
                         specialties='x',
                         department='x',
                         course='x',
                         group='x',
                         coursework='x',
                         knowledge='x')
    worker1 = Worker(telegram_id='0',
                     worker_name='x',
                     name='ww',
                     login='1',
                     password='1')
    session.add(worker1)
    session.commit()
    # note that the Engineer table is not INSERTed into

    #student1 = session.query(User).filter_by(telegram_id="1").one()
    # the next line triggers an exception because it tries to lookup
    # the Engineer row, which is missing
    #print(student1.eng_data)
except Exception as e:
    print(e)"""

"""Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = Student(student_id=2,
                   student_name='TEST',
                   university='KUB',
                   faculty='WWW',
                   specialties='Q',
                   department='E',
                   course="1",
                   group='12',
                   coursework='NO',
                   knowledge="NO")
session.add(new_user)
session.commit()

student = session.query(Student).all()
for s in student:
    print(s.student_id, s.student_name, s.course)"""