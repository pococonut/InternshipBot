from sqlalchemy import create_engine, Column, Integer, Boolean, String
from dotenv import load_dotenv
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


class Application(Base):
    __tablename__ = "application"

    # telegram user id
    application_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # ФИО
    student_id = Column(String, unique=True)

    worker_id = Column(String)

    approve = Column(Boolean)


Base.metadata.create_all(bind=engine)

