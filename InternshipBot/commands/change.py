from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from commands.general import get_keyboard, check_param
from keyboard import change_ikb, change_worker_ikb, back_ikb
from db.commands import select_user, user_type, change_inform

check_d = {'student_name': 'ФИО',
           'phone': 'Номер телефона',
           'university': 'ВУЗ',
           'faculty': 'Факультет',
           'specialties': 'Направление',
           'department': 'Кафедра',
           'course': 'Курс',
           'group': 'Группа',
           'coursework': 'Курсовые работы',
           'knowledge': 'Знания', }

student_params = list(check_d.keys())
param_for_change = {}


class ChangeUser(StatesGroup):
    parameter = State()
    new_value = State()


def change_keyboard(t_id):
    """
    Функция возвращающая клавиатуру с параметрами доступными для изменения в зависимости от типа пользователя.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :return k: Inline-клавиатура.
    """

    user_exist = select_user(t_id)
    if not user_exist:
        return None

    u_type = user_type(t_id)
    if u_type[0] == 'student':
        return change_ikb
    return change_worker_ikb


@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    """
    Функция, возвращающая клавиатуру с параметрами, доступными для изменения.
    """

    keyboard = change_keyboard(message.from_user.id)
    if keyboard is None:
        msg_text = 'Вы еще не зарегистрированы.\nПройдите этап регистрации.'
        await message.answer(msg_text)
        return

    msg_text = 'Выберите параметр, который желаете изменить.'
    await message.answer(msg_text, reply_markup=keyboard)
    await ChangeUser.parameter.set()


@dp.callback_query_handler(text='change')
async def change_inline(callback: types.CallbackQuery):
    """
    Функция, возвращающая клавиатуру с параметрами, доступными для изменения.
    """

    keyboard = change_keyboard(callback.from_user.id)
    if keyboard is None:
        msg_text = 'Вы еще не зарегистрированы.\nПройдите этап регистрации.'
        await callback.message.edit_text(msg_text)
        return

    msg_text = 'Выберите параметр, который желаете изменить.'
    await callback.message.edit_text(msg_text, reply_markup=keyboard)
    await ChangeUser.parameter.set()


@dp.callback_query_handler(text=student_params, state=ChangeUser.parameter)
async def get_param_student(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция получения нового значения параметра, выбранного для изменения.
    """

    user_id = str(callback.from_user.id)
    param_for_change[user_id] = callback.data

    await state.update_data(parameter=callback.data)
    await callback.message.edit_text("Введите новое значение.", reply_markup=back_ikb)
    await ChangeUser.next()


@dp.message_handler(state=ChangeUser.new_value)
async def get_val_student(message: types.Message, state: FSMContext):
    """
    Функция проверки и установки нового значения параметра, выбранного для изменения.
    """

    user_id = str(message.from_user.id)
    parameter = param_for_change[user_id]
    new_value = message.text
    result_change = check_param(parameter, new_value)

    if not result_change:
        msg_text = "Значение введено в некорректном формате. Повторите ввод."
        await message.answer(msg_text)
        return

    await state.update_data(new_value=result_change)
    data = await state.get_data()

    u_type = user_type(user_id)[0]
    keyboard = get_keyboard(user_id)
    change_inform(user_id, u_type, data['parameter'], data['new_value'])
    msg_text = (f"<b>Параметр:</b> {check_d.get(data['parameter'])}\n"
                f"<b>Новое значение:</b> {data['new_value']}\n"
                f"Параметр изменен.")

    await message.answer(msg_text, parse_mode='HTML', reply_markup=keyboard)
    param_for_change.clear()
    await state.finish()
