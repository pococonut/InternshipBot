import re
import os
import json
import string
import logging

import phonenumbers
from aiogram.dispatcher.filters.state import StatesGroup, State

from db.commands import select_task, select_user


class ConfirmDeletion(StatesGroup):
    delete = State()


def short_long_task(task, flag=0):
    """
    Функция вывода данных задачи.
    :param task: Строка модели БД, относящаяся к конкретной задаче, с информацией о ней.
    :param flag: Булево значение, 1 - вывод всей информации задачи, 0 - вывод краткой информации задачи.
    :return: Строка с информацией о задаче.
    """

    s = f"<b>Название:</b> {task.task_name}\n\n" \
        f"<b>Цель:</b> {task.task_goal}\n\n" \
        f"<b>Описание:</b> {task.task_description}\n\n" \
        f"<b>Необходимые навыки и технологии:</b>\n{task.task_technologies}\n\n"

    if flag:
        s += f"<b>Задачи:</b>\n{task.task_tasks}\n\n" \
             f"<b>Умения и навыки, получаемые в процессе " \
             f"прохождения практики:</b>\n{task.task_new_skills}\n\n" \
             f"<b>Количество людей:</b> {task.num_people}\n\n" \
             f"<b>Материалы:</b>\n{str(task.materials)}\n\n"

    if select_user(task.from_id):
        s += f"<b>Сотрудник:</b> <a href='tg://user?id={task.from_id}'>{select_user(task.from_id).name}</a>"

    return s


def get_tasks_for_student():
    """
    Функция получения списка задач для студентов
    :return: список задач для студентов
    """

    return [t for t in select_task() if not t.student_id or (len(t.student_id.split()) != int(t.num_people))]


def check_user_name(name):
    """
    Функция для валидации ФИО
    name: ФИО пользователя
    :return: True - ФИО корректно, False - ФИО некорректно
    """

    if len(name) > 60:
        return False

    if len(name.split()) != 3:
        return False

    no_numbers = name.replace(" ", "").replace("-", "").isalpha()
    if not no_numbers:
        return False

    name = " ".join([w.capitalize() for w in name.split()])
    return name


def check_symbols(value):
    """
    Функция для проверки отсутствия в строке цифр и символов
    :param value: Строка для проверки
    :return: False - есть запрещенные символы,
             True - нет запрещенных символов
    """

    if any(chr.isdigit() for chr in value):
        return False
    if any(chr in string.punctuation for chr in value):
        return False
    return value.upper()


def check_phone(value):
    """
    Функция для проверки формата номера телефона
    :param value: Строка для проверки
    :return: Номер телефона, если он правильный, иначе False
    """

    try:
        phonenumbers.parse(value)
        return value
    except:
        return False


def check_university(value):
    """
    Функция для проверки формата написания названия университета
    :param value: Строка для проверки
    :return: название университета, если написание правильное, иначе False
    """

    if len(value.split()) != 1:
        return False
    if not check_symbols(value):
        return False
    return value.upper()


def check_course(value):
    """
    Функция для проверки формата написания курса
    :param value: Строка для проверки
    :return: Курс, если написание правильное, иначе False
    """

    if len(value) != 1:
        return False
    if any(chr in string.punctuation for chr in value):
        return False
    return value


def check_group(value):
    """
    Функция для проверки формата написания группы
    :param value: Строка для проверки
    :return: Группа, если написание правильное, иначе False
    """

    if re.fullmatch('\d{,3}\D\d', value) is None:
        return False
    if ' ' in value or any(chr.isalpha() for chr in value):
        return False
    if any(chr in string.punctuation.replace('/', '') for chr in value):
        return False
    return value


def check_len_txt(value):
    """
    Функция для проверки максимальной длинны сообщения
    :param value: Строка для проверки
    :return: Сообщение, если длинна не превышает максимальное значение, иначе False
    """

    if len(value) > 200:
        return False
    return value


def check_user_parameter(parameter, value):
    """
    Функция проверки параметра заявки на корректность.
    :param parameter: Название параметра, который пользователь хочет изменить.
    :param value: Введенное пользователем новое значение параметра.
    :return: Возвращает введенное значение, если оно прошло проверку, иначе возвращает False.
    """

    parameters = {"student_name": check_user_name,
                  "phone": check_phone,
                  "university": check_university,
                  "faculty": check_symbols,
                  "specialties": check_symbols,
                  "department": check_symbols,
                  "course": check_course,
                  "group": check_group,
                  "coursework": check_len_txt,
                  "knowledge": check_len_txt}

    return parameters[parameter](value)


def check_len_parameter(parameter, max_length):
    """
    Функция для проверки длины вводимого параметра
    :param parameter: Параметр
    :param max_length: Максимальная длинна параметра
    :return: False - если длинна параметра превышает допустимое значение, иначе True
    """

    if len(parameter.split()) > max_length:
        return False
    return True


def check_num_people(parameter):
    """
    Функция для проверки параметра задачи - "Количество людей"
    :param parameter: Количество людей введенное пользователем
    :return: False - при неправильном формате параметра, иначе True
    """

    if not parameter.isdigit():
        return False
    if len(parameter.split()) > 1:
        return False
    if any(chr.isalpha() for chr in parameter):
        return False
    if int(parameter) > 5:
        return False
    return True


def check_task_parameter(parameter, value=None):
    """
    Функция проверки параметра задачи на корректность.
    :param parameter: Название параметра, который пользователь хочет изменить.
    :param value: Введенное пользователем новое значение параметра.
    :return: Возвращает введенное значение, если оно прошло проверку, иначе возвращает False.
    """

    parameters = {"change_task_name": (check_len_parameter, 50),
                  "change_task_goal": (check_len_parameter, 50),
                  "change_task_description": (check_len_parameter, 200),
                  "change_task_tasks": (check_len_parameter, 500),
                  "change_task_technologies": (check_len_parameter, 200),
                  "change_task_new_skills": (check_len_parameter, 200),
                  "change_num_people": (check_num_people, value),
                  "change_materials": (check_len_parameter, 200)}

    func,  func_value = parameters[parameter]

    if not value:
        return func(func_value)
    return func(value, func_value)


def read_user_values(dict_name):
    """
    Функция для чтения переменных пользователя, используемых при взаимодействии с ботом
    Args:
        dict_name: Название словаря с переменными

    Returns: Словарь с переменными
    """

    filename = "user_values.json"
    try:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='UTF-8') as f:
                json.dump({}, f)

        with open(filename, 'r', encoding='UTF-8') as file:
            data = json.load(file)
            g_dict = data.get(f'{dict_name}', {})
            return g_dict

    except FileNotFoundError:
        logging.warning(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError:
        logging.warning(f"Error decoding JSON from file {filename}.")
        return {}


def write_user_values(dict_name, g_dict):
    """
    Функция для записи переменных пользователя, используемых при взаимодействии с ботом
    Args:
        dict_name: Название словаря с переменными
        g_dict: Словарь с переменными

    Returns: None
    """

    filename = "user_values.json"
    try:
        with open(filename, 'r', encoding='UTF-8') as file:
            data = json.load(file)
            data[f'{dict_name}'] = g_dict

        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file)
    except Exception as e:
        logging.exception(e)


def print_stud(s, c=None):
    """
    Функция возвращающая данные студента в виде строки.
    :param s:  Строка модели БД, относящаяся к конкретному студенту, с информацией о нем.
    :param c:  Кнопка.
    :return: Строка с данными студента.
    """

    if c is None:
        stud = f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n\n"
    else:
        stud = f"<b>ФИО:</b> <a href='tg://user?id={s.telegram_id}'>{s.student_name}</a>\n"
    stud += f"<b>Номер телефона:</b> <code>{s.phone}</code>\n"\
            f"<b>ВУЗ:</b> {s.university}\n" \
            f"<b>Факультет:</b> {s.faculty}\n" \
            f"<b>Специальность:</b> {s.specialties}\n" \
            f"<b>Кафедра:</b> {s.department}\n" \
            f"<b>Курс:</b> {s.course}\n" \
            f"<b>Группа:</b> {s.group}\n\n" \
            f"<b>Курсовые:</b> {s.coursework}\n\n" \
            f"<b>Знания:</b> {s.knowledge}\n\n" \
            f"<b>Дата регистрации:</b> {s.reg_date}\n\n"
    return stud


def navigation(direction, page, count):
    """
    Функция для навигации по списку объектов.
    :param direction: Направление (Вперед, Назад).
    :param page: Текущая номер объекта.
    :param count: Количество объектов.
    :return: Строка, Номер объекта.
    """

    if 'right' in direction:
        page += 1
        if page == count:
            page = 0
        num = page
        if page <= -1:
            num = count + page
        s = f"<b>№</b> {num + 1}/{count}\n\n"
        return s, page

    if 'left' in direction:
        page -= 1
        num = 0
        if page == (-1) * count:
            page = 0
        if page <= -1:
            num = count
        s = f"<b>№</b> {(num + page) + 1}/{count}\n\n"
        return s, page