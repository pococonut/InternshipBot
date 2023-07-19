from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, String, ForeignKey
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
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

