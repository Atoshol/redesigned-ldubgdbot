from typing import Any

import requests


def check_group(group_name: str) -> tuple[bool, Any]:
    res = requests.get('https://rozklad.ldubgd.edu.ua/cgi-bin/'
                       'timetable_export.cgi?req_type=obj_list&req_mode=group&'
                       'show_ID=yes&req_format=json&coding_mode=UTF8&bs=ok')
    lst_groups = []
    name = []
    try:
        for deps in res.json()['psrozklad_export']['departments']:
            for group in deps['objects']:
                lst_groups.append(group['name'])
                if group_name.lower()[:3] == group['name'].lower()[:3]:
                    name.append(group['name'])
        return (False, name) if group_name not in lst_groups else (True, name)
    except:
        return False, ''
