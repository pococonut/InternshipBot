from aiogram.utils import executor
from create import dp
from aiogram import types
from db.models.user import Base, engine
from commands import registration, change, show, authorization, task_add, task_actions, task_actions_worker,\
    applications, task_selected_student, task_selected_worker, back, user_add, export_data, get_menu

commands = [
    types.BotCommand(command='/menu', description='Меню'),
    types.BotCommand(command='/change', description='Изменение данных'),
    types.BotCommand(command='/show', description='Просмотр данных'),
]


async def set_commands(dp):
    await dp.bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats())


DESCRIPTION = "Данный телеграм бот предназначен для работы с практиками," \
              " с которыми можно ознакомиться после регистрации и одобрения заявки сотрудниками."


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать!\n\n" + DESCRIPTION)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)
