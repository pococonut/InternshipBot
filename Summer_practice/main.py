from aiogram.utils import executor
from create import dp
from aiogram import types
from commands import registration, change, show, authorization, task_add, task_actions, task_actions_worker,\
    applications, task_selected_student, task_selected_worker, back, user_add


commands = [
    types.BotCommand(command='/student', description='Меню студента'),
    types.BotCommand(command='/menu', description='Меню сотрудника'),
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


def print_stud(s):
    stud = f"<b>ФИО:</b> {s.student_name}\n\n" \
           f"<b>ВУЗ:</b> {s.university}\n\n" \
           f"<b>Факультет:</b> {s.faculty}\n\n" \
           f"<b>Специальность:</b> {s.specialties}\n\n" \
           f"<b>Кафедра:</b> {s.department}\n\n" \
           f"<b>Курс:</b> {s.course}\n\n" \
           f"<b>Группа:</b> {s.group}\n\n" \
           f"<b>Курсовые:</b> {s.coursework}\n\n" \
           f"<b>Знания:</b> {s.knowledge}\n\n" \
           f"<b>Дата регистрации:</b> {s.reg_date}\n"
    return stud


registration.register_handlers_registration(dp)
change.register_handlers_change(dp)
show.register_handlers_show(dp)
authorization.register_handlers_authorization(dp)
task_add.register_handlers_task_add(dp)
task_actions.register_handlers_task_actions(dp)
task_actions_worker.register_handlers_task_actions_worker(dp)
applications.register_handlers_applications(dp)
task_selected_student.register_handlers_task_selected_student(dp)
task_selected_worker.register_handlers_task_selected_worker(dp)
user_add.register_handlers_add_user(dp)
back.register_handlers_back(dp)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)
