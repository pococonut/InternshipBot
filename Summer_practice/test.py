"""from aiogram import Bot, Dispatcher, types

TOKEN_API = "6392143741:AAHR9cXnhECcoQdiJTrV37l7eRDTljnqmEQ"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)  # инициализация входящих данных


# отправка фото
@dp.message_handler(commands=['picture'])
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://avatars.mds.yandex.net/i?id=e3a09207c9a26de5f24e9405d36303e65e4269a6-9234742-images-thumbs&n=13')


# отправка сткера
@dp.message_handler(commands=['give'])
async def give_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJjPdkoDIPMFK1HhHBqU-TAkjB8Uv5PgACOhYAAn-JAUh6cv99Dl9CzC8E")
    await message.delete()


# ответ на сообшения с добавлением эмоджи к исходному текту
@dp.message_handler()
async def send_emoji(message: types.Message):
    await message.reply(message.text + "🌸")


# отправка id стикера
@dp.message_handler(content_types=['sticker'])
async def send_sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id)


@dp.callback_query_handler()
async def reg_callback(callback: types.CallbackQuery):
    if callback.data == 'new':
        await callback.answer(text='Введите ФИО в формате: Иванов Иван Иванович')
    if callback.data == 'change':
        await callback.answer(text='Выберите параметр, который желаете изменить')
    if callback.data == 'show':
        await callback.answer(text='Ваша заявка:')"""

"""@dp.callback_query_handler(text='change')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer('Выберите параметр, который желаете изменить', reply_markup=change_ikb)
    await Changings.get_student_name.set()

    s_id = int(callback.from_user.id)


    @dp.callback_query_handler(text="student_name")
    async def f_callback(callback: types.CallbackQuery):
        await callback.message.edit_reply_markup()
        await callback.message.delete()

        print('FUUUUUUCKKK')
        # if callback.data == 'student_name':

        if select_student(s_id) is None:
            await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
        else:
            await callback.message.answer('Введите ФИО', parse_mode='HTML')

            @dp.message_handler(state=Changings.get_student_name)
            async def txt1(message: types.Message, state: FSMContext):
                s_name = message.text
                print(s_name)
                if len(s_name.split()) != 3 or any(chr.isdigit() for chr in s_name) or any(
                        chr in string.punctuation for chr in s_name):
                    await callback.message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, " ".join(i.capitalize() for i in s_name.split(' ')))
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                    await state.update_data(student_name=message.text)
                    await Changings.address.set()
                    print(s_name)


    @dp.callback_query_handler(text="university")
    async def f_callback(callback: types.CallbackQuery):
        await callback.message.edit_reply_markup()
        await callback.message.delete()

        if select_student(s_id) is None:
            await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
        else:
            await callback.message.answer('Введите ВУЗ', parse_mode='HTML')

            @dp.message_handler(state=Changings.get_university)
            async def txt2(message: types.Message, state: FSMContext):
                university = message.text
                print(university)
                if len(university.split()) != 1 or any(chr.isdigit() for chr in university) or any(
                        chr in string.punctuation for chr in university):

                    await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, university.upper())
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')

                    print(university)
                    await state.update_data(university=message.text)
                    data = await state.get_data()
                    await message.answer(f"Имя: {data['student_name']}\n"
                                         f"Адрес: {data['university']}")

                    await state.finish()
"""

"""
@dp.callback_query_handler(text='university')
async def f_callback(callback: types.CallbackQuery):
    print('!!!!!!!! ', callback.data)
    s_id = int(callback.from_user.id)

    # print('FUUUUUUCKKK')
    # if callback.data == 'student_name':

    if select_student(s_id) is None:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
    else:
        await callback.message.answer('Введите данные', parse_mode='HTML')

        @dp.message_handler()
        async def txt1(message: types.Message):

            get_txt(message.text)
            print("get text", message.text)
            if message.text:
                if callback.data == 'university':
                    print('university: ', callback.data)

                    print('Параметр: ', callback.data)
                    if select_txt() != []:
                        ch[1] = select_txt()[0][0]
                        print(ch[0])
                        if (len(university.split()) != 1 or any(chr.isdigit() for chr in university) or any(
                                chr in string.punctuation for chr in university)):
                            await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                        else:
                            change_stud_inform(s_id, callback.data, university.upper())
                            await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                            print("delete")
                            delete_txt()"""

"""case "input_again_btn":
            texting_from_keyboard(callback)
        case "no_answer_btn":
            texting_from_keyboard(callback)
        case "yes_answer_btn":
            find_dish_btn_clicked_keyboard(callback)
        case "input_ingr_again_btn":
            try_to_delete_lst_bot_msg(callback.message.chat.id)
            Clear_all_user_data_without_lst_mes_id(callback.message.chat.id)
            texting_from_keyboard(callback)

..............

@bot.message_handler(content_types='text')
def texting_from_keyboard(callback):
    try:
        try_to_delete_lst_bot_msg(callback.message.chat.id)
    except:
        pass
    msg = bot.send_message(callback.message.chat.id, 'Вводите ваши ингредиенты через запятую - "картофель, говядина...:"')
    bot.register_next_step_handler(msg, input_ingredients_from_keyboard)
    Set_LastMessageId_by_UserID(msg.id, callback.message.chat.id)


def input_ingredients_from_keyboard(message):
    lst_id = int(str(user_data_db.return_user_last_message_id(message.chat.id))[1:-2])
    ingr_to_db = procedure_check_user_ingr(str(message.text), message.chat.id)
    if ingr_to_db == False:
        markup = types.InlineKeyboardMarkup(row_width=1)
        input_again_btn = types.InlineKeyboardButton(text=f'Ввести заново', callback_data='input_again_btn')
        markup.add(input_again_btn)
        bot.edit_message_text(chat_id=message.chat.id, message_id=lst_id, text=f'Попробуйтe ввести ингредиенты заново {emoji.return_confused_face()}', reply_markup=markup)
        Set_LastMessageId_by_UserID(lst_id, message.chat.id)

    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes_answer_btn = types.InlineKeyboardButton(text=f'Да{emoji.return_beaming_face_with_smiling_eyes()}', callback_data='yes_answer_btn')
        no_answer_btn = types.InlineKeyboardButton(text=f'Нет{emoji.return_upside_down_face()}', callback_data='no_answer_btn')
        markup.add(yes_answer_btn, no_answer_btn)
        ingredients_to_show = str(user_data_db.return_user_Ingredients_Show_toQuerry(message.chat.id))[3:-4]
        bot.edit_message_text(chat_id=message.chat.id, message_id=lst_id, text=mes_to_user.confirm_the_ingredients()+str(f'{ingredients_to_show}'), reply_markup=markup)
        Set_LastMessageId_by_UserID(lst_id, message.chat.id)

        msg = bot.send_message(message.chat.id,
                               f'Скорее выбирай, а то я уже грею сковородку {emoji.return_pan_with_egg()}')
        Set_LastMessageId_by_UserID(msg.id, message.chat.id)"""

"""
lst = []
@dp.callback_query_handler(text='new')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    if callback.data == 'new':
        # print(s_id)
        student_exist = select_student(s_id)
        if student_exist:
            await callback.message.answer('Вы уже зарегестрированы', parse_mode='HTML', reply_markup=ikb_3)
            await callback.message.edit_reply_markup()
            await callback.message.delete()
        else:
            await callback.message.answer(FORM, parse_mode='HTML')
            await callback.message.answer('Введите ФИО', parse_mode='HTML')

            @dp.message_handler()
            async def student_name(message: types.Message):

                if message.chat.type == 'private':
                    if len(lst) != 9:
                        txt = message.text
                        # lst.append(message.text)

                        if len(lst) == 8:
                            lst.append(txt)

                        if len(lst) == 7:
                            lst.append(txt)
                            await callback.message.answer('Введите ваши знания', parse_mode='HTML')

                        if len(lst) == 6:
                            if any(chr.isalpha() for chr in txt) or any(
                                    chr in string.punctuation.replace('./', '') for chr in txt):
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
                                await callback.message.answer('Кафедра введена в неккоректом формате',
                                                              parse_mode='HTML')
                            else:
                                lst.append(txt)
                                await callback.message.answer('Введите Курс', parse_mode='HTML')

                        if len(lst) == 3:
                            if any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Направление введено в неккоректом формате',
                                                              parse_mode='HTML')
                            else:
                                lst.append(txt.capitalize())
                                await callback.message.answer('Введите Кафедру', parse_mode='HTML')

                        if len(lst) == 2:
                            if any(chr.isdigit() for chr in txt) or any(chr in string.punctuation for chr in txt):
                                await callback.message.answer('Факультет введен в неккоректом формате',
                                                              parse_mode='HTML')
                            else:
                                lst.append(txt.capitalize())
                                await callback.message.answer('Введите Направление', parse_mode='HTML')

                        if len(lst) == 1:
                            if len(txt.split()) != 1 or any(chr.isdigit() for chr in txt) or any(
                                    chr in string.punctuation for chr in txt):
                                await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                            else:
                                lst.append(txt.upper())
                                await callback.message.answer('Введите Факультет', parse_mode='HTML')

                        if len(lst) == 0:
                            if len(txt.split()) != 3 or any(chr.isdigit() for chr in txt) or any(
                                    chr in string.punctuation for chr in txt):
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
                                await callback.message.answer('Регистрация окончена.', parse_mode='HTML',
                                                              reply_markup=ikb_2)"""

"""
@dp.message_handler(filters.Text(startswith=["отмена", "в главное меню"], ignore_case=True), state="*")
async def button_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:  
        await state.finish()
    await message.answer("Операция отменена.", reply_markup=keyboards.users)"""

"""
@dp.callback_query_handler(text='student_name')
async def f_callback(callback: types.CallbackQuery):
    print('!!!!!!!! ', callback.data)
    s_id = int(callback.from_user.id)

    if select_student(s_id) is None:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
    else:
        await callback.message.answer('Введите данные', parse_mode='HTML')

        if callback.data == 'student_name':
            print('s_name: ', callback.data)

            print('Параметр: ', callback.data)

            if select_txt() != []:
                txt = select_txt()[0][0]
                print(txt)

                if (len(txt.split()) != 3 or any(chr.isdigit() for chr in txt) or any(
                        chr in string.punctuation for chr in txt)):
                    await callback.message.answer('ФИО введено в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, " ".join(i.capitalize() for i in txt.split(' ')))
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                    print("delete")
                    delete_txt()


@dp.callback_query_handler(text='university')
async def f_callback(callback: types.CallbackQuery):
    print('!!!!!!!! ', callback.data)
    s_id = int(callback.from_user.id)

    # print('FUUUUUUCKKK')
    # if callback.data == 'student_name':

    if select_student(s_id) is None:
        await callback.message.answer('Вы пока не зарегестрированы', parse_mode='HTML')
    else:
        await callback.message.answer('Введите данные', parse_mode='HTML')

        if callback.data == 'university':
            print('university: ', callback.data)

            print('Параметр: ', callback.data)

            if select_txt() != []:

                university = select_txt()[0][0]

                if (len(university.split()) != 1 or any(chr.isdigit() for chr in university) or any(
                        chr in string.punctuation for chr in university)):
                    await callback.message.answer('ВУЗ введен в неккоректом формате', parse_mode='HTML')
                else:
                    change_stud_inform(s_id, callback.data, university.upper())
                    await callback.message.answer('Параметр обновлен', parse_mode='HTML')
                    print(university)
                    """

"""
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

"""@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    student_exist = select_student(message.from_user.id)
    if not student_exist:
        await message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    else:
        await message.answer(f'Введите номер параметра, который желаете изменить:\n\n'
                             f'ФИО - 1\n\n'
                             f'ВУЗ - 2\n\n'
                             f'Факультет - 3\n\n'
                             f'Направление - 4\n\n'
                             f'Кафедра - 5\n\n'
                             f'Курс - 6\n\n'
                             f'Группа - 7\n\n'
                             f'Темы курсовых работ - 8\n\n'
                             f'Ваши знания - 9\n\n',
                             reply_markup=back_ikb
                             )
        await Change_student.param.set()


@dp.callback_query_handler(text='back', state="*")
async def back_func(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer('Действие отменено.')


@dp.message_handler(state=Change_student.param)
async def get_param(message: types.Message, state=FSMContext):
    if message.text not in chek_d:
        await message.answer("Вы ввели неверный параметр.\nПожалуйста, повторите ввод.")
        return
    change_d['p'] = message.text
    print(message.text)
    await state.update_data(param=message.text)
    await message.answer("Введите новое значение.")
    await Change_student.next()


@dp.message_handler(state=Change_student.new_val)
async def get_val(message: types.Message, state: FSMContext):
    if chek_param(change_d['p'], message.text) is False:
        await message.answer("Вы ввели значение в некоректном  формате.\n\n Пожалуйста, повторите ввод.")
        return

    change_d['v'] = message.text
    await state.update_data(new_val=message.text)
    data = await state.get_data()
    await message.answer(f"Параметр: {chek_d.get(data['param'])[1]}\n\n"
                         f"Новое значение: {data['new_val']}")

    k = chek_d.get(data['param'])[0]
    v = data['new_val']
    change_stud_inform(message.from_user.id, k, v)

    await message.answer('Параметр изменен.', parse_mode='HTML', reply_markup=ikb_3)  # reply_markup=ikb_2
    await state.finish()"""

"""
@dp.callback_query_handler(text='show')
async def reg_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()

    s_id = int(callback.from_user.id)
    user_show = select_user(s_id)
    print(user_show)
    if user_show.type == 'student':
        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.student_name}\n\n"
                                      f"ВУЗ: {user_show.university}\n\n"
                                      f"Факультет: {user_show.faculty}\n\n"
                                      f"Специальность: {user_show.specialties}\n\n"
                                      f"Кафедра: {user_show.department}\n\n"
                                      f"Курс: {user_show.course}\n\n"
                                      f"Группа: {user_show.group}\n\n"
                                      f"Курсовые: {user_show.coursework}\n\n"
                                      f"Знания: {user_show.knowledge}\n\n"
                                      f"Дата регистрации: {user_show.reg_date}\n\n"
                                      )
    elif user_show.type != 'student':
        await callback.message.answer(f"Ваши данные\n\n"
                                      f"ФИО: {user_show.admin_name}\n\n")

    else:
        await callback.message.answer('Вы еще не зарегестрированы.\nПожалуйста, пройдите этап регистрации.',
                                      parse_mode='HTML')"""


"""
page_tws = 0


@dp.callback_query_handler(text='worker_chosen_tasks')
async def worker_chosen_t(callback: types.CallbackQuery):
    global page_tws
    page_tws = 0
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        try:
            student = select_user(tasks[0].student_id)
            await callback.message.edit_text(f"<b>№</b> {page_tws + 1}/{tasks}\n\n"
                                             f"👨‍🎓<b>Студент</b>\n\n"
                                             f"<b>ФИО:</b> {student.student_name}\n\n"
                                             f"<b>Направление:</b> {student.specialties}\n\n"
                                             f"<b>Курс:</b> {student.course}\n\n"
                                             f"<b>Знания:</b> {student.knowledge}\n\n"
                                             f"——————————————————\n\n"
                                             f"📚<b>Выбранная задача</b>\n\n"
                                             f"<b>Название:</b> {tasks[0].task_name}\n\n"
                                             f"<b>Описание:</b> {tasks[0].task_description}\n\n",
                                             parse_mode='HTML',
                                             reply_markup=task_worker_stud,
                                             disable_web_page_preview=True)
        except Exception as e:
            print(e)


@dp.callback_query_handler(text=['tws_right', 'tws_left'])
async def task_ws_show(callback: types.CallbackQuery):
    global page_tws
    tasks = select_chosen_tasks(callback.from_user.id)
    if not tasks:
        await callback.message.edit_text('Ваши задачи еще не выбраны.', reply_markup=admin_ikb)
    else:
        count_tasks = len(tasks)
        s = ''
        if callback.data == 'tws_right':
            page_tws += 1
            if page_tws == count_tasks:
                page_tws = 0
            p_tws = page_tws
            if page_tws <= -1:
                p_tws = count_tasks + page_tws
            s = f"<b>№</b> {p_tws + 1}/{count_tasks}\n\n"

        elif callback.data == 'tws_left':
            page_tws -= 1
            p_tws = 0
            if page_tws == (-1) * count_tasks:
                page_tws = 0
            if page_tws <= -1:
                p_tws = count_tasks
            s = f"<b>№</b> {(p_tws + page_w) + 1}/{count_tasks}\n\n"

        student = select_user(tasks[page_tws].student_id)
        await callback.message.edit_text(s + f"👨‍🎓<b>Студент</b>\n\n"
                                         f"<b>ФИО:</b> {student.student_name}\n\n"
                                         f"<b>Направление:</b> {student.specialties}\n\n"
                                         f"<b>Курс:</b> {student.course}\n\n"
                                         f"<b>Знания:</b> {student.knowledge}\n\n"
                                         f"——————————————————\n\n"
                                         f"📚<b>Выбранная задача</b>\n\n"
                                         f"<b>Название:</b> {tasks[page_tws].task_name}\n\n"
                                         f"<b>Описание:</b> {tasks[page_tws].task_description}\n\n",
                                         parse_mode='HTML',
                                         reply_markup=task_worker_stud,
                                         disable_web_page_preview=True)"""

@dp.callback_query_handler(text='left_stud')
async def std_left(callback: types.CallbackQuery):
    global page_stud
    all_students = select_students()
    applications = select_applications()
    count_students = len(all_students) - len(applications)
    students = [s for s in all_students if s.telegram_id not in [i.student_id for i in applications]]
    if not students:
        await callback.message.edit_text('В данный момент заявок нет.\nЗагляните позже.', reply_markup=admin_ikb)
    else:
        page_stud -= 1
        p_ls = 0
        if page_stud == (-1) * count_students:
            page_stud = 0
        if page_stud <= -1:
            p_ls = count_students
        print(p_ls, page_stud)

        await callback.message.edit_text(
            f"<b>№</b> {(p_ls + page_stud) + 1}/{count_students}\n\n" + print_stud(students, page_stud),
            reply_markup=stud_appl_ikb, parse_mode='HTML')