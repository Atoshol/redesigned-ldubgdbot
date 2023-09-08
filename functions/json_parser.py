from functions.get_date import get_name_of_week_by_date
from functions.string_former import str_format


def json_parser(res, status):
    data = {}
    for i in res:
        date = i['date']
        day_name = get_name_of_week_by_date(date)
        try:
            data[day_name].append(str_format(i, status))
        except KeyError:
            data[day_name] = [str_format(i, status)]
    return data
