from sqlalchemy import Column, Integer, Boolean, String

from db.models.user import Base


class Application(Base):
    """Модель таблицы результатов просмотра заявок студентов.
       :application_id: Уникальный идентификатор таблицы.
       :student_id: идентификатор студента в телеграм.
       :worker_id: идентификатор сотрудника, отклонившего/одобрившего заявку, в телеграм.
       :approve: Состояние заявки, 1 - принят, 0 - не принят.
    """

    __tablename__ = "application"
    application_id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    student_id = Column(String, unique=True)
    worker_id = Column(String)
    approve = Column(Boolean)


