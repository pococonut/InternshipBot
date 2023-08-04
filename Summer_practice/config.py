from pydantic import BaseSettings


class Settings(BaseSettings):
    api: str = "6392143741:AAEsx0nMPsI3CBm_fGHOnw8npgWVnOcmp0g"
    host: str = "localhost"
    password: str = "123"
    database: str = "bot"

#5432
settings = Settings()