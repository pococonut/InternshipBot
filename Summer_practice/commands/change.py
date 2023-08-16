from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import phonenumbers
import string
import re

from commands.back import back_func
from db.commands import select_user, user_type, change_inform
from keyboard import change_ikb, change_worker_ikb, admin_ikb, worker_ikb, ikb_3, back_ikb


# -------------------- Изменение данных --------------------


def chek_param(p, v):
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


class ChangeUser(StatesGroup):
    par = State()
    new_val = State()


chek_d = {'student_name': 'ФИО',
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

stud_params, s_p = list(chek_d.keys()), []


def change_keyboard(t_id):
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


async def change(message: types.Message):
    keyboard = change_keyboard(message.from_user.id)
    if keyboard is None:
        await message.answer('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    else:
        await message.answer(f'Выберите параметр, который желаете изменить.', reply_markup=keyboard)
        await ChangeUser.par.set()


async def change_inline(callback: types.CallbackQuery):
    keyboard = change_keyboard(callback.from_user.id)
    if keyboard is None:
        await callback.message.edit_text('Вы еще не зарегистрированы.\nПожалуйста, пройдите этап регистрации.', parse_mode='HTML')
    else:
        await callback.message.edit_text(f'Выберите параметр, который желаете изменить.', reply_markup=keyboard)
        await ChangeUser.par.set()


async def get_param_student(callback: types.CallbackQuery, state=FSMContext):
    await state.update_data(par=callback.data)
    s_p.append(callback.data)
    await callback.message.edit_text("Введите новое значение.", reply_markup=back_ikb)
    await ChangeUser.next()


async def get_val_student(message: types.Message, state: FSMContext):
    x = chek_param(s_p[0], message.text)
    if not x:
        await message.answer("Значение введено в некорректном формате. Повторите ввод.")
        return
    s_p.clear()
    await state.update_data(new_val=x)
    data = await state.get_data()
    await message.answer(f"<b>Параметр:</b> {chek_d.get(data['par'])}\n\n"
                         f"<b>Новое значение:</b> {data['new_val']}", parse_mode='HTML')
    u_type = user_type(message.from_user.id)[0]
    change_inform(message.from_user.id, u_type, data['par'], data['new_val'])
    keyboard = admin_ikb
    if u_type == 'worker':
        keyboard = worker_ikb
    elif u_type == 'student':
        keyboard = ikb_3
    await message.answer('Параметр изменен.', parse_mode='HTML', reply_markup=keyboard)
    await state.finish()


def register_handlers_change(dp: Dispatcher):
    dp.register_message_handler(change, commands=['change'])
    dp.register_callback_query_handler(change_inline, text='change')
    dp.register_callback_query_handler(get_param_student, text=stud_params, state=ChangeUser.par)
    dp.register_message_handler(get_val_student, state=ChangeUser.new_val)
    dp.register_callback_query_handler(back_func, text='back', state="*")
