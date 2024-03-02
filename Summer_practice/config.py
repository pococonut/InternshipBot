from dotenv import load_dotenv
from pydantic import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    api: str = os.getenv("API")
    host: str = os.getenv("HOST")
    password: str = os.getenv("DB_PASSWORD")
    database: str = os.getenv("DB_NAME")


settings = Settings()