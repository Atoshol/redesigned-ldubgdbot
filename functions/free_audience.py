import requests
from functions.get_date import *


def audience(lesson_number):
    """take lesson_number and return list of empty audience"""

    data = get_audience(lesson_number)[0]["rooms"]

    rooms_by_block = {}
    for lesson in data:
        if lesson['block'] in ["НК 1", "!!! НК 3 (Клепарівська,22)", "НК 2", "НК 4", "НК 5"]:
            try:
                rooms_by_block[lesson["block"].replace('!', '')].append(lesson["name"])
            except KeyError:
                rooms_by_block[lesson["block"].replace('!', '')] = [lesson["name"]]

    return rooms_by_block


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
