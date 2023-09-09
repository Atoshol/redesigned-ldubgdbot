from copy import deepcopy
from ldubgdbot.bot.keyboards.reply import KB_SCHEDULE
from ldubgdbot.bot.keyboards.inline import KB_SCHEDULE_WEEK
from aiogram import Dispatcher, Bot
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import Message, CallbackQuery
from functions.get_date import *
from ldubgdbot.bot.database.methods.get import *
from functions.get_politek import *
from functions.json_parser import *
from ldubgdbot.bot.filters.main import IsStudent


async def __schedule_student_choose(msg: Message):
    kb = deepcopy(KB_SCHEDULE)
    await msg.answer("Обери:", reply_markup=kb)


async def __schedule_student_send1(msg: Message):
    user_id = msg.from_user.id
    if msg.text == 'На Сьогодні':
        lessonDate = get_day_date()
    else:
        lessonDate = get_next_day_date()

    status = get_status_by_id(user_id)
    student_id = get_student_id(user_id)
    id_s, username, f_name, status_of_subs, group_id = get_student_data(student_id)
    group_name = get_group_name_by_id(group_id)
    group_id = get_group_id_by_name_politek(group_name)

    res = get_rozklad_by_group(group_id, start_date=lessonDate, end_date=lessonDate)

    if res:
        data = json_parser(res, status)
        loguru.logger.info(f' 200 {user_id}')
        for key, value in data.items():
            value = sorted(value, key=lambda value: int(value[3:4]))
            await msg.answer(hbold(key) + ':\n' + ''.join(value))
    else:
        await msg.answer('Розкладу не знайдено.')
        return 'BAD request'


async def __schedule_student_send_callback_kb(msg: Message):
    kb = deepcopy(KB_SCHEDULE_WEEK)
    await msg.answer("Обери:", reply_markup=kb)


async def __schedule_student_week_callback(query: CallbackQuery):
    bot: Bot = query.bot
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = deepcopy(KB_SCHEDULE_WEEK)

    today = datetime.date.today()

    if get_name_of_week_by_date(today.strftime("%d.%m.%Y")) in ['Субота', 'Неділя']:
        date_week = today + datetime.timedelta(days=3)
    else:
        date_week = today

    current_week = [d for d in get_week(date_week)]
    lessonDateStart = current_week[1].replace('-', '.')
    lessonDateEnd = current_week[-1].replace('-', '.')

    user_id = query.from_user.id
    student_id = get_student_id(user_id)
    id_s, username, f_name, status_of_subs, group_id = get_student_data(student_id)
    group_name = get_group_name_by_id(group_id)
    group_id = get_group_id_by_name_politek(group_name)
    res = get_rozklad_by_group(group_id, lessonDateStart, lessonDateEnd)
    status = get_status_by_id(user_id)

    loguru.logger.info(f' 200 {user_id}')

    if res:
        data = json_parser(res, status)
        if query.data != 'Завершити перегляд':
            try:
                value = data[query.data]
                value = sorted(value, key=lambda value: int(value[3:4]))
                to_send = hbold(query.data) + ':' + '\n' + ''.join(value)
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                            text=to_send, reply_markup=markup)
            except:
                try:
                    text = 'Не знайдено'
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                                reply_markup=markup)
                except MessageNotModified:
                    pass
        else:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

    else:
        await query.answer('Розкладу не знайдено.')
    await query.answer()


def register_student_handlers(dp: Dispatcher):

    dp.register_message_handler(__schedule_student_choose, IsStudent(),
                                content_types=["text"], text="Розклад🗓")
    dp.register_message_handler(__schedule_student_send1, IsStudent(),
                                content_types=["text"], text="На Сьогодні")
    dp.register_message_handler(__schedule_student_send1, IsStudent(),
                                content_types=["text"], text="На Завтра")
    dp.register_message_handler(__schedule_student_send_callback_kb, IsStudent(),
                                content_types=["text"], text="На Тиждень")
    dp.register_callback_query_handler(__schedule_student_week_callback, IsStudent())
