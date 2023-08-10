from sqlalchemy import create_engine, Column, VARCHAR, String, Integer
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


class AddedUser(Base):
    __tablename__ = "added_user"

    id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    telegram_id = Column(String, nullable=True)
    login = Column(VARCHAR(50), unique=True, nullable=False)
    password = Column(VARCHAR(50), unique=True, nullable=False)
    type = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(30), nullable=True)
    name = Column(VARCHAR(50), nullable=True)


Base.metadata.create_all(bind=engine)
