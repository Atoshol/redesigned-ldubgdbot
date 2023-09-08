from typing import Final
from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration_state(StatesGroup):
    CHOOSE_OF_STATUS: Final = State()
    CHOOSE_OF_GROUP: Final = State()
    TEACHER_NAME_STATE: Final = State()
    REG_INTO_DB: Final = State()


class Feedback_state(StatesGroup):
    init_state: Final = State()
    answer_state: Final = State()


class Free_audience(StatesGroup):
    init_state: Final = State()
    answer_state: Final = State()


class Search_state(StatesGroup):
    choose_type: Final = State()
    input_data: Final = State()
    input_date: Final = State()
    send_response: Final = State()


class Teacher_send_message(StatesGroup):
    get_group: Final = State()
    get_subject: Final = State()
    get_message: Final = State()
    send_message: Final = State()
