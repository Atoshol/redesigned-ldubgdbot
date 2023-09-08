import datetime
import pandas as pd
from aiogram.utils.markdown import hbold

one_day = datetime.timedelta(days=1)


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.

  'date' may be a datetime or date instance (the same type is returned).
  """
    day_idx = (date.weekday() + 1) % 7  # turn sunday into 0, monday into 1, etc.
    sunday = date - datetime.timedelta(days=day_idx)
    date = sunday
    for n in range(7):
        yield date.strftime("%d.%m.%Y")
        date += one_day


def get_day_date() -> str:
    """ Return str date of current day """

    now = datetime.datetime.now()
    dt_string = now.strftime("%d.%m.%Y")
    return dt_string


def get_next_day_date() -> str:
    """ Return str date of tomorrow """

    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=1)
    dt_string = yesterday.strftime("%d.%m.%Y")
    return dt_string


def get_second_day() -> str:
    """ Return str date of day after tomorrow """

    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=2)
    dt_string = yesterday.strftime("%d.%m.%Y")
    return dt_string


def get_name_of_week_by_date(date) -> str:
    """ Return day name """

    temp = pd.Timestamp(f'{date[3:5]}.{date[0:2]}.{date[6:]}')
    day_name = temp.day_name()
    days = [('Sunday', 'Неділя'),
            ('Monday', "Понеділок"),
            ('Tuesday', "Вівторок"),
            ('Wednesday', "Середа"),
            ('Thursday', "Четвер"),
            ('Friday', "П'ятниця"),
            ('Saturday', "Субота")]
    for day in days:
        if day_name in day:
            day_name = day[1]
    return day_name
