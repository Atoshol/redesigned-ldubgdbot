from copy import deepcopy
from functions import get_data
from ldubgdbot.bot.keyboards.reply import *


def get_start_keyboard(user_id: int) -> tuple:
    status = get_data.get_status_by_id(user_id)
    kb = deepcopy(KB_START_BOT if not status else KB_GO_TO_MENU)
    return kb, status


def get_menu_keyboard(user_id: int) -> tuple:
    status = get_data.get_status_by_id(user_id)
    kb = deepcopy(KB_START_BOT if not status else KB_MENU)
    if status == 'admin':
        pass
    elif status == 'teacher':
        kb.add(KeyboardButton("Надіслати повідомлення студентам"))
        kb.row(KeyboardButton("Розклад🗓"))
    else:
        kb.row(KeyboardButton("Розклад🗓"))
    # kb_menu.add(types.KeyboardButton("Пошук вільної авдиторії🔍"))
    kb.row(KeyboardButton("Посібник📕"), KeyboardButton("Корисні посилання📚"))
    kb.add(KeyboardButton("Написати відгук/Повідомити про помилку📮"))
    kb.add(KeyboardButton("Видалити реєстрацію❌"))
    return kb, status


def get_registration_keyboard(user_id: int) -> tuple:
    status = get_data.get_status_by_id(user_id)
    kb = deepcopy(KB_REGISTRATION)
    return kb, status


