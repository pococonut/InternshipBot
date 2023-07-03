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




