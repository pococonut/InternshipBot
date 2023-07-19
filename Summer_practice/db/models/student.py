from sqlalchemy import create_engine, Column, VARCHAR, TEXT, DATE, Integer
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


class Student(Base):
    __tablename__ = "student"

    # telegram user id
    student_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    # ФИО
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

    # telegram user name
    # username = Column(VARCHAR(32), unique=False, nullable=True)
    # registration date
    reg_date = Column(DATE, default=datetime.date.today())
    # last update date
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"<Student:{(self.student_id)}>"


Base.metadata.create_all(bind=engine)
