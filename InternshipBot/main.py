import logging

from aiogram.utils import executor
from aiogram import types

from create import dp
from db.models.user import Base, engine
from keyboard import new_user_ikb
from commands import registration, user_change, user_show, authorization, task_add, task_actions, task_actions_worker, \
    applications, task_selected_student, task_selected_worker, back, account_add, export_data, get_menu, task_change, \
    task_delete, account_show, account_delete


DESCRIPTION = "Данный телеграм бот предназначен для работы с практиками," \
              " с которыми можно ознакомиться после регистрации и одобрения заявки сотрудниками."


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать!\n\n" + DESCRIPTION, reply_markup=new_user_ikb)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    executor.start_polling(dp, skip_updates=True)
