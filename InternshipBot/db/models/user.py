import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, String, ForeignKey
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

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
    """Модель таблицы пользователей.

        :telegram_id: Уникальный идентификатор пользователя в телеграм.

        :type: Тип пользователя (student, admin, director, worker).
        :name: ФИО пользователя.
        :phone: Номер телефона пользователя, привязанного к телеграм.

        :reg_date: Дата регистрации.
        :upd_date: Дата последнего изменения личных параметров.
    """

    __tablename__ = "user"

    telegram_id = Column(String, unique=True, nullable=False, primary_key=True, )

    type = Column(VARCHAR(50), nullable=False)

    name = Column(VARCHAR(50), nullable=False)

    phone = Column(VARCHAR(30), nullable=False)

    reg_date = Column(DATE, default=datetime.date.today())

    upd_date = Column(DATE, onupdate=datetime.date.today())

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }


class Student(User):
    """Модель таблицы студентов.

        :telegram_id: Уникальный идентификатор пользователя в телеграм.

        :student_name: ФИО студента.
        :university: Название университета.
        :faculty: Название факультета.
        :specialties: Название специальности.
        :department: Название кафедры.
        :course: Номер курса.
        :group: Номер группы.
        :coursework: Название и описание курсовых работ.
        :knowledge: Описание знаний студента.
    """

    __tablename__ = "student"

    telegram_id = Column(String, ForeignKey(User.telegram_id), primary_key=True)

    student_name = Column(VARCHAR(50), nullable=False)

    university = Column(VARCHAR(100), nullable=False)

    faculty = Column(VARCHAR(100), nullable=False)

    specialties = Column(VARCHAR(100), nullable=False)

    department = Column(VARCHAR(100), nullable=True)

    course = Column(VARCHAR(10), nullable=False)

    group = Column(VARCHAR(10), nullable=False)

    coursework = Column(TEXT, nullable=True)

    knowledge = Column(TEXT, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Worker(User):
    """Модель таблицы сотрудников.

        :telegram_id: Уникальный идентификатор пользователя в телеграм.

        :worker_name: ФИО сотрудника.
        :login: Логин пользователя.
        :password: Пароль пользователя.
    """

    __tablename__ = "worker"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    worker_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "worker",
    }


class Admin(User):
    """Модель таблицы администраторов.

        :telegram_id: Уникальный идентификатор пользователя в телеграм.

        :worker_name: ФИО пользователя.
        :login: Логин пользователя.
        :password: Пароль пользователя.
    """

    __tablename__ = "admin"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    admin_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Director(User):
    """Модель таблицы директоров.

        :telegram_id: Уникальный идентификатор пользователя в телеграм.

        :worker_name: ФИО пользователя.
        :login: Логин пользователя.
        :password: Пароль пользователя.
    """

    __tablename__ = "director"

    telegram_id = Column(String, ForeignKey("user.telegram_id"), primary_key=True)

    director_name = Column(VARCHAR(50), nullable=False)

    login = Column(String, nullable=False, primary_key=True)

    password = Column(String, unique=True, nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "director",
    }


Base.metadata.create_all(bind=engine)

