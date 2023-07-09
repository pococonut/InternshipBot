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
    telegram_id = Column(String, unique=True, nullable=False, primary_key=True, )
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


class Admin(User):
    __tablename__ = "admin"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    admin_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Director(User):
    __tablename__ = "director"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    director_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "director",
    }


Base.metadata.create_all(bind=engine)



"""
try:
    student1 = Student_2(telegram_id='0',
                         student_name='Золотухина Полина Викторовна',
                         name='Золотухина Полина Викторовна',
                         university="КУБГУ",
                         faculty="Математика и компьютерные науки",
                         specialties='Математика и компьютерные науки',
                         department='ВМИ',
                         course='2',
                         group='23/3',
                         coursework='1)Разработка парсера для телеграм канала',
                         knowledge='Python, SQL')
    worker1 = Worker(telegram_id='1',
                     worker_name='Золотухина Полина Викторовна',
                     name='Золотухина Полина Викторовна',
                     login='1',
                     password='2')

    admin1 = Admin(telegram_id="1103049875",
                   admin_name='Золотухина Полина Викторовна',
                   name='Золотухина Полина Викторовна',
                   login='1',
                   password='111')

    director1 = Director(telegram_id='3',
                         director_name='Золотухина Полина Викторовна',
                         name='Золотухина Полина Викторовна',
                         login='1',
                         password='4')
    session.add(student1)

    #session.add(admin1)
    #session.add(director1)

    session.commit()
    # note that the Engineer table is not INSERTed into

    # student1 = session.query(User).filter_by(telegram_id="1").one()
    # the next line triggers an exception because it tries to lookup
    # the Engineer row, which is missing
    # print(student1.eng_data)
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
