import requests
import loguru


def get_group_id_by_name_politek(group_name):
    res = requests.get("https://rozklad.ldubgd.edu.ua/cgi-bin/timetable_export.cgi"
                       "?req_type=obj_list&req_mode=group&show_ID=yes&"
                       "req_format=json&coding_mode=UTF8&bs=ok")
    loguru.logger.info(f"{res}")
    try:
        if res.json():
            group_id = 0
            for inst in res.json()["psrozklad_export"]["departments"]:
                for groups in inst["objects"]:
                    if groups["name"] == group_name:
                        group_id = groups["ID"]
                        break
            return group_id
    except:
        return []


def get_teacher_id_by_name_politek(f_name, m_name, l_name):
    res = requests.get("https://rozklad.ldubgd.edu.ua/cgi-bin/timetable_export.cgi"
                       "?req_type=obj_list&req_mode=teacher&show_ID=yes&"
                       "req_format=json&coding_mode=UTF8&bs=ok")
    loguru.logger.info(f"{res}")
    try:
        if res.json():
            try:
                teacher_id = 0
                for inst in res.json()["psrozklad_export"]["departments"]:
                    for teacher in inst["objects"]:
                        if f_name == teacher["I"] and m_name == teacher["B"] and l_name == teacher["P"]:
                            teacher_id = teacher["ID"]
                return teacher_id
            except:
                return []
    except:
        return []


def get_rozklad_by_group(group_id, start_date="", end_date=""):
    BASE = 'https://rozklad.ldubgd.edu.ua/cgi-bin/timetable_export.cgi?'

    params = {"req_type": "rozklad",
              "req_mode": "group",
              "OBJ_ID": f"{group_id}",
              "OBJ_name": "",
              "dep_name": "",
              "ros_text": "separated",
              "show_empty": "",
              "begin_date": f"{start_date}",
              "end_date": f"{end_date}",
              "req_format": "json",
              "coding_mode": "UTF8",
              "bs": "ok"}

    res = requests.get(BASE, params=params)
    loguru.logger.info(f"{res}")
    try:
        rozklad_json = res.json()["psrozklad_export"]["roz_items"]
    except:
        rozklad_json = []
    return rozklad_json


def get_rozklad_by_teacher(teacher_id, start_date="", end_date=""):
    BASE = 'https://rozklad.ldubgd.edu.ua/cgi-bin/timetable_export.cgi?'

    params = {"req_type": "rozklad",
              "req_mode": "teacher",
              "OBJ_ID": f"{teacher_id}",
              "OBJ_name": "",
              "dep_name": "",
              "ros_text": "separated",
              "show_empty": "",
              "begin_date": f"{start_date}",
              "end_date": f"{end_date}",
              "req_format": "json",
              "coding_mode": "UTF8",
              "bs": "ok"}

    res = requests.get(BASE, params=params)
    loguru.logger.info(f"{res}")
    try:
        rozklad_json = res.json()["psrozklad_export"]["roz_items"]
    except:
        rozklad_json = []
    return rozklad_json
