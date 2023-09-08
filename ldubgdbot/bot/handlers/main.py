from aiogram import Dispatcher

from ldubgdbot.bot.handlers.student.main import register_student_handlers
from ldubgdbot.bot.handlers.teacher.main import register_teacher_handlers
from ldubgdbot.bot.handlers.other.main import register_other_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_student_handlers,
        register_teacher_handlers,
        register_other_handlers
    )
    for handler in handlers:
        handler(dp)
