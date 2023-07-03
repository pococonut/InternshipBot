from aiogram import Bot, Dispatcher, executor, types
from keyboard import ikb, kb, ikb2
import string
from commands import register_student, select_student


TOKEN_API = "6392143741:AAHR9cXnhECcoQdiJTrV37l7eRDTljnqmEQ"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)  # инициализация входящих данных

HELP_COMMAND = """
<b>/help</b> - список комманд
<b>/description</b> - описание бота
<b>/registration</b> - регистрация студента
<b>/authorisation</b> - авторизация персонала
"""

DESCRIPTION = """
Данный телеграм бот предназначен для рабты с практиками и стажировками, с которыми можно ознакомиться после регистрации и подачи заявок
"""

FORM = """
Введите данные <b>отдельными сообщениями</b>.

<b>ФИО</b> в формате: <em>Иванов Иван Иванович</em>

<b>ВУЗ</b> в формате: <em>КУБГУ</em>

<b>Факультет</b> в формате: <em>Математика и компьютерные науки</em>

<b>Направление</b> в формате: <em>Математика и компьютерные науки</em>

<b>Кафедра</b> (при отсутствии введите: "Нет") в формате: <em>ВМИ</em>

<b>Курс</b> в формате: <em>2</em>

<b>Группа</b> в формате: <em>23/3</em>

<b>Темы курсовых работ</b> (при отсутствии введите: "Нет") в формате: <em>1)Разработка сайта для КУБГУ, 2)Калькулятор матриц</em>

<b>Ваши знания</b> (при отсутствии введите: "Нет") в формате: <em>Python, SQL, C++, JS</em>
"""


async def on_startup(_):
    print("Бот запущен")


# описание бота
@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer(DESCRIPTION)
    await message.delete()


# помощь
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND, parse_mode='HTML')


# старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Добро пожаловать!",
                         reply_markup=kb)
    # await message.delete()  # удаляем сообщение пользователя, которое он отправил


@dp.message_handler(commands=['registration'])
async def registration_command(message: types.Message):
    await message.answer(text="Выберите опцию:",
                         reply_markup=ikb)


lst = []
@dp.callback_query_handler()
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    if callback.data == 'new':
        #print(s_id)
        student_exist = select_student(s_id)
        if student_exist:
            await callback.message.answer('Вы уже зарегестрированы', parse_mode='HTML')
        else:
            await callback.message.answer(FORM, parse_mode='HTML')
            await callback.message.answer('Введите ФИО', parse_mode='HTML')

            @dp.message_handler()
            async def student_name(message: types.Message):

                if message.chat.type == 'private':
                    if len(lst) != 9:
                        txt = message.text
                        #lst.append(message.text)

                        if len(lst) == 8:
                            lst.append(txt)

                        if len(lst) == 7:
                            lst.append(txt)
                            await callback.message.answer('Введите ваши знания', parse_mode='HTML')

                        if len(lst) == 6:
                            if any(chr.isalpha() for chr in txt) or any(chr in string.punctuation.replace('./','') for chr in txt):
                                await callback.message.answer('Группа введена в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt)
                                await callback.message.answer('Введите Темы курсовых работ', parse_mode='HTML')

                        if len(lst) == 5:
                            if any(chr.isalpha() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Курс введен в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt)
                                await callback.message.answer('Введите Группу', parse_mode='HTML')

                        if len(lst) == 4:
                            if any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Кафедра введена в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt)
                                await callback.message.answer('Введите Курс', parse_mode='HTML')

                        if len(lst) == 3:
                            if any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Направление введено в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt.capitalize())
                                await callback.message.answer('Введите Кафедру', parse_mode='HTML')

                        if len(lst) == 2:
                            if any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Факультет введен в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt.capitalize())
                                await callback.message.answer('Введите Направление', parse_mode='HTML')

                        if len(lst) == 1:
                            if len(txt.split()) != 1 or any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt.upper())
                                await callback.message.answer('Введите Факультет', parse_mode='HTML')

                        if len(lst) == 0:
                            if len(txt.split()) != 3 or any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(" ".join(i.capitalize() for i in txt.split(' ')))
                                await callback.message.answer('Введите ВУЗ', parse_mode='HTML')

                        if len(lst) == 9:
                            await callback.message.answer(f'Ваши данные:\n\n'
                                                          f'{lst[0]}\n\n'
                                                          f'{lst[1]}\n\n'
                                                          f'{lst[2]}\n\n'
                                                          f'{lst[3]}\n\n'
                                                          f'{lst[4]}\n\n'
                                                          f'{lst[5]}\n\n'
                                                          f'{lst[6]}\n\n'
                                                          f'{lst[7]}\n\n'
                                                          f'{lst[8]}\n', parse_mode='HTML')
                            print(lst)
                            student = register_student(s_id, lst)
                            if student:
                                await callback.message.answer('Регистрация окончена.', parse_mode='HTML')
                            #else:
                            #    await callback.message.answer('Вы уже зарегестрированы', parse_mode='HTML')

    elif callback.data == 'change':
        await callback.message.answer('Выберите параметр, который желаете изменить')
    elif callback.data == 'show':

        student_show = select_student(s_id)
        if student_show:

            await callback.message.answer(f"Ваши данные\n\n"
                                          f"ФИО: {student_show.student_name}\n\n"
                                          f"ВУЗ: {student_show.university}\n\n"
                                          f"Факультет: {student_show.faculty}\n\n"
                                          f"Специальность: {student_show.specialties}\n\n"
                                          f"Кафедра: {student_show.department}\n\n"
                                          f"Курс: {student_show.course}\n\n"
                                          f"Группа: {student_show.group}\n\n"
                                          f"Курсовые: {student_show.coursework}\n\n"
                                          f"Знания: {student_show.knowledge}\n\n"
                                          f"Дата регистрации: {student_show.reg_date}\n\n"
                                          )
        else:
            await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
