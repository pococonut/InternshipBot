from sqlalchemy import Column, VARCHAR, Integer
from db.models.user import Base


class AddedUser(Base):
    """Модель таблицы добавленных аккаунтов.

        :id: Уникальный идентификатор аккаунта.

        :login: Логин аккаунта.
        :password: Пароль аккаунта.

        :type: Тип аккаунта (student, admin, director, worker).
        :name_usr: ФИО пользователя (В случае, если пользователь авторизовался).
    """

    __tablename__ = "added_user"

    id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)

    login = Column(VARCHAR(50), unique=True, nullable=False)

    password = Column(VARCHAR(50), unique=True, nullable=False)

    type = Column(VARCHAR(50), nullable=False)
    
    name_usr = Column(VARCHAR(100))

