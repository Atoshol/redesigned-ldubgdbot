import requests


def check_teacher(f_name: str, m_name: str, l_name: str) -> tuple:
    res = requests.get('https://rozklad.ldubgd.edu.ua/cgi-bin/'
                       'timetable_export.cgi?req_type=obj_list&req_mode=teacher'
                       '&show_ID=yes&req_format=json&coding_mode=UTF8&bs=ok')
    for departments in res.json()['psrozklad_export']['departments']:
        for obj in departments['objects']:
            name_from_res_f = obj['I']
            name_from_res_m = obj['B']
            name_from_res_l = obj['P']

            if f_name == name_from_res_f \
                    and m_name == name_from_res_m \
                    and l_name == name_from_res_l:
                dep = departments['name']
                return f_name, m_name, l_name, dep
    return ()
