from aiogram import Dispatcher
from aiogram.dispatcher.filters import Filter
from aiogram.types import Message
from ldubgdbot.bot.database.methods.get import get_status_by_id


class IsStudent(Filter):
    key = 'is_student'

    async def check(self, msg: Message) -> bool:
        status = get_status_by_id(msg.from_user.id)
        return True if status == 'student' else False


class IsTeacher(Filter):
    key = 'is_teacher'

    async def check(self, msg: Message):
        status = get_status_by_id(msg.from_user.id)
        return True if status == 'teacher' else False


def register_all_filters(dp: Dispatcher):
    filters = (
        IsStudent,
        IsTeacher,
    )
    for filter in filters:
        dp.bind_filter(filter)
