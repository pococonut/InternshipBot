
# InternshipBot

## Описание проекта

InternshipBot - это телеграм бот, предназначеный для работы с практиками и стажировками. Цель этого проекта заключается в упрощении и оптимизации процессов, связанных с задачами, которые могут возникнуть как у студентов, так и у сотрудников компании во время проведения стажировок. Бот предоставляет различные функциональности, в зависимости от роли пользователя (студент, сотрудник, руководитель, администратор).
\
\
На данный момент телеграм-бот предоставляет следующие возможности:

Для студента:
- Поэтапная регистрация и заполнение заявки студентами, включающая ввод личных данных, информации о месте обучения, а также о проектах и знаниях студента.
- Возможность изменения параметров заявки.
- Выбор задачи от организации. Студент может отказаться от выбранной задачи и выбрать другую, если необходимо.

Для директора/администатора:
- Добавление, удаление, редактирование, просмотр всех задач.
- Одобрение/отклонение заявок на стажировку.
- Экспорт данных в формате Excel.
- Управление аккаунтами сотрудников.
- Просмотр выбранных студентами задач.
- Радактирование личных данных.

Для сотрудников:
- Добавление, удаление, редактирование своих задач, а также просмотр всех задач.
- Просмотр выбранных студентами задач сотрудника.
- Редактирование личных данных.

При разработке был использован язык программирования Python, асинхронный фреймворк для Telegram Bot API - aiogram, библиотека SQLAlchemy, позволяющая описывать структуры баз данных и способы взаимодействия с ними на языке Python без использования SQL, а так же реляционная база данных PostgreSQL.
