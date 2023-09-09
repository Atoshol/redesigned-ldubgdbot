import json
from functions.get_date import *
from aiogram.utils.markdown import hbold
from datetime import datetime, timedelta


def get_sec_plus_para(time_str):
    """ Get Seconds from time """

    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s) + 4800


def get_sec_plus_hour(time_str):
    """ Get Seconds from time """

    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s) + 3600


def str_format(lesson_data: dict, status) -> str:
    """ Take dict with lessons from DB and return string for message """

    pattern = ''
    les_id = lesson_data['lesson_number']
    sub_name = lesson_data['title']
    if status == 'teacher':
        teacher = lesson_data["object"]
    else:
        teacher = lesson_data['teacher']
    audience = lesson_data['room']
    if audience == '':
        audience = lesson_data['object']
    les_type = lesson_data['type']
    date = lesson_data['date']
    lesson_time = lesson_data['lesson_time']
    group = lesson_data['group']
    if group == "" and status == 'student':
        group = lesson_data['object']
    comment = lesson_data['replacement']
    pattern += f'{hbold(str(les_id) + ".")} {hbold(sub_name)}\n' \
               f'{"Викладач:"} {hbold(teacher)}\n' \
               f'{"Авдиторія:"} {hbold(audience)}\n' \
               f'{"Тип заняття:"} {hbold(les_type)}\n' \
               f'{"Дата:"} {hbold(date)}\n' \
               f'{"Початок заняття:"} {hbold(lesson_time)}\n' \
               f'{"Група/и:"} {hbold(group)}\n' \
               f'{"Коментар: " + comment if comment != "" else ""}\n\n'
    return pattern
