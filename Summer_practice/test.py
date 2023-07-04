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