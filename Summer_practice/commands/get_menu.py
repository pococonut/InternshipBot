from create import dp
from aiogram import types
from db.commands import user_type
from commands.general import get_keyboard
from keyboard import new_user_ikb, chat_ikb


@dp.message_handler(commands=['menu'])
async def menu_get(message: types.Message):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """
    user_exist = user_type(message.from_user.id)
    if not user_exist:
        await message.answer(
            f'Выберите команду.\n<em>Регистрация</em> -  Для студентов.\n'
            f'<em>Авторизация</em> - Для сотрудников.', parse_mode='HTML', reply_markup=new_user_ikb)
    else:
        keyboard = get_keyboard(message.from_user.id)
        await message.answer(f'Выберите команду.', parse_mode='HTML', reply_markup=keyboard)


@dp.callback_query_handler(text='menu')
async def menu_get_inline(callback: types.CallbackQuery):
    """
    Функция получения меню для зарегистрированного пользователя и авторизации/регистрации для незарегистрированного.
    """
    keyboard = get_keyboard(callback.from_user.id)
    await callback.message.edit_text("Выберите команду.", parse_mode='HTML', reply_markup=keyboard)


@dp.callback_query_handler(text='chat')
async def chat_command(callback: types.CallbackQuery):
    """
    Функция возвращающая ссылку на общий чат.
    """
    await callback.message.edit_text("Чат для связи доступен по ссылке - https://t.me/+FShhqiWUDJRjODky.",
                                     disable_web_page_preview=True, reply_markup=chat_ikb)