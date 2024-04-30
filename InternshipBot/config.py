import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

load_dotenv()


class Settings(BaseSettings):
    api: str = os.getenv("API")
    host: str = os.getenv("HOST")
    password: str = os.getenv("POSTGRES_PASSWORD")
    database: str = os.getenv("POSTGRES_DB")


settings = Settings()

load_dotenv()

host = settings.host
password = settings.password
database = settings.database

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}:5432/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()