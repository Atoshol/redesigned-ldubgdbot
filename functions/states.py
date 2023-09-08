from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration_state(StatesGroup):
    choose_of_status = State()
    choose_of_group = State()
    teacher_name_state = State()
    registration_into_bd = State()


class Qr_state(StatesGroup):
    get_photo_state = State()
    answer_state = State()


class Feedback_state(StatesGroup):
    init_state = State()
    answer_state = State()


class Free_audience(StatesGroup):
    init_state = State()
    answer_state = State()


class Search_state(StatesGroup):
    choose_type = State()
    input_data = State()
    input_date = State()
    send_response = State()


class Teacher_send_message(StatesGroup):
    get_group = State()
    get_subject = State()
    get_message = State()
    send_message = State()
