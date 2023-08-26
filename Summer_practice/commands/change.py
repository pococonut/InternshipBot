import re
import string
import phonenumbers
from create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from commands.general import get_keyboard
from keyboard import change_ikb, change_worker_ikb, back_ikb
from db.commands import select_user, user_type, change_inform
from aiogram.dispatcher.filters.state import StatesGroup, State


check_d = {'student_name': 'ФИО',
           'phone': 'Номер телефона',
           'university': 'ВУЗ',
           'faculty': 'Факультет',
           'specialties': 'Направление',
           'department': 'Кафедра',
           'course': 'Курс',
           'group': 'Группа',
           'coursework': 'Курсовые работы',
           'knowledge': 'Знания',
           }

stud_params, s_p = list(check_d.keys()), []


class ChangeUser(StatesGroup):
    par = State()
    new_val = State()


def check_param(p, v):
    """
    Функция проверки параметра заявки на корректность.
    :param p: Название параметра, который пользователь хочет изменить.
    :param v: Введенное пользователем новое значение параметра.
    :return: Возвращает введенное значение, если оно прошло проверку, иначе возвращает False.
    """
    if p == 'student_name':
        if len(v.split()) != 3 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return " ".join([i.capitalize() for i in v.split()])
    elif p == 'phone':
        try:
            phonenumbers.parse(v)
            return v
        except:
            return False
    elif p == 'university':
        if len(v.split()) != 1 or any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.upper()
    elif p == 'faculty':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.capitalize()
    elif p == 'specialties':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.capitalize()
    elif p == 'department':
        if any(chr.isdigit() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v.upper()
    elif p == 'course':
        if len(v) != 1 or any(chr.isalpha() for chr in v) or any(chr in string.punctuation for chr in v):
            return False
        else:
            return v
    elif p == 'group':
        if ((re.fullmatch('\d{,3}\D\d', v) is None) or ' ' in v or any(chr.isalpha() for chr in v) or any(
                chr in string.punctuation.replace('/', '') for chr in v)):
            return False
        else:
            return v
    elif p == 'coursework' or 'knowledge':
        if len(v) > 200:
            return False
        else:
            return v

    return v


def change_keyboard(t_id):
    """
    Функция возвращающая клавиатуру с параметрами доступными для изменения в зависимости от типа пользователя.
    :param t_id: Уникальный идентификатор пользователя в телеграм.
    :return k: Inline-клавиатура.
    """
    user_exist = select_user(t_id)
    if not user_exist:
        k = None
    else:
        u_type = user_type(t_id)
        if u_type[0] == 'student':
            k = change_ikb
        else:
            k = change_worker_ikb
    return k


@dp.message_handler(commands=['change'])
async def change(message: types.Message):
    """
    Функция, возвращающая клавиатуру с параметрами, доступными для изменения.
    """
    keyboard = change_keyboard(message.from_user.id)
    if keyboard is None:
        await message.answer('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    else:
        await message.edit_text(f'Выберите параметр, который желаете изменить.', reply_markup=keyboard)
        await ChangeUser.par.set()


@dp.callback_query_handler(text='change')
async def change_inline(callback: types.CallbackQuery):
    """
    Функция, возвращающая клавиатуру с параметрами, доступными для изменения.
    """
    keyboard = change_keyboard(callback.from_user.id)
    if keyboard is None:
        await callback.message.edit_text('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.',
                                         parse_mode='HTML')
    else:
        await callback.message.edit_text(f'Выберите параметр, который желаете изменить.', reply_markup=keyboard)
        await ChangeUser.par.set()


@dp.callback_query_handler(text=stud_params, state=ChangeUser.par)
async def get_param_student(callback: types.CallbackQuery, state=FSMContext):
    """
    Функция получения нового значения параметра, выбранного для изменения.
    """
    await state.update_data(par=callback.data)
    s_p.append(callback.data)
    await callback.message.edit_text("Введите новое значение.", reply_markup=back_ikb)
    await ChangeUser.next()


@dp.message_handler(state=ChangeUser.new_val)
async def get_val_student(message: types.Message, state: FSMContext):
    """
    Функция проверки и установки нового значения параметра, выбранного для изменения.
    """
    x = check_param(s_p[0], message.text)
    if not x:
        await message.answer("Значение введено в некорректном формате. Повторите ввод.")
        return
    s_p.clear()
    await state.update_data(new_val=x)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {check_d.get(data['par'])}\n\n"
                         f"<b>Новое значение:</b> {data['new_val']}", parse_mode='HTML')
    u_type = user_type(message.from_user.id)[0]
    change_inform(message.from_user.id, u_type, data['par'], data['new_val'])
    keyboard = get_keyboard(message.from_user.id)
    await message.answer('Параметр изменен.', parse_mode='HTML', reply_markup=keyboard)
    await state.finish()
