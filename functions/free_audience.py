import requests
from functions.get_date import *


def audience(lesson_number):
    """take lesson_number and return list of empty audience"""

    data = get_audience(lesson_number)[0]["rooms"]

    lst_rooms = []
    rooms_by_floor = {}
    for lesson in data:
        if lesson["block"] == "НК 1":
            try:
                rooms_by_floor[lesson["name"][0]].append(lesson["name"])
            except KeyError:
                rooms_by_floor[lesson["name"][0]] = [lesson["name"]]
    print(rooms_by_floor)
    try:
        pattern = f"Вільні аудиторії: \n" \
                  f"  {hbold('1 Поверх:')}\n" \
                  f"    {', '.join(rooms_by_floor['1'])}\n" \
                  f"  {hbold('2 Поверх:')}\n" \
                  f"    {', '.join(rooms_by_floor['2'])}\n" \
                  f"  {hbold('3 Поверх:')}\n" \
                  f"    {', '.join(rooms_by_floor['3'])}\n" \
                  f"  {hbold('4 Поверх:')}\n" \
                  f"    {', '.join(rooms_by_floor['4'])}\n"
        return pattern
    except KeyError:
        return 'Не знайдено'


def get_audience(lesson_number) -> list or None:
    """get data from politek"""

    date = get_day_date()

    BASE = 'https://rozklad.ldubgd.edu.ua/cgi-bin/timetable_export.cgi?'

    params = {"req_type": "free_rooms_list",
              "req_mode": "group",
              "OBJ_ID": f"",
              "OBJ_name": "",
              "dep_name": "",
              "ros_text": "separated",
              "show_empty": "",
              "begin_date": f"{date}",
              "end_date": f"{date}",
              "lesson": f"{lesson_number}",
              "req_format": "json",
              "coding_mode": "UTF8",
              "bs": "ok"}

    res = requests.get(BASE, params=params)
    try:
        return res.json()["psrozklad_export"]["free_rooms"]
    except KeyError:
        return None
