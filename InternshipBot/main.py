from aiogram.utils import executor
from aiogram import types
from create import dp
from db.models.user import Base, engine
from commands import registration, change, show, authorization, task_add, task_actions, task_actions_worker,\
    applications, task_selected_student, task_selected_worker, back, user_add, export_data, get_menu
from keyboard import new_user_ikb


DESCRIPTION = "Данный телеграм бот предназначен для работы с практиками," \
              " с которыми можно ознакомиться после регистрации и одобрения заявки сотрудниками."


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать!\n\n" + DESCRIPTION, reply_markup=new_user_ikb)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)