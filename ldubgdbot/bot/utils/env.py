import os
from abc import ABC
from typing import Final


class Env(ABC):
    TOKEN: Final = os.environ.get('TOKEN')
    database: Final = os.environ.get('database')
    host: Final = os.environ.get('host')
    username: Final = os.environ.get('username')
    password: Final = os.environ.get('password')
    FEEDBACK_CHAT_ID = os.environ.get('feedback')
