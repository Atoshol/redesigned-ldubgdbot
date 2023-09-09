from copy import deepcopy
from ldubgdbot.bot.keyboards.reply import KB_SCHEDULE, KB_FREE_AUDIENCE, KB_GO_TO_MENU
from ldubgdbot.bot.keyboards.inline import KB_SCHEDULE_WEEK
from aiogram import Dispatcher, Bot
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import Message, CallbackQuery
from functions.get_date import *
from ldubgdbot.bot.database.methods.get import *
from functions.get_politek import *
from functions.json_parser import *
from ldubgdbot.bot.filters.main import IsTeacher
from ldubgdbot.bot.utils.states import Free_audience
from functions.free_audience import audience
import loguru
from aiogram.dispatcher.storage import FSMContext


async def __schedule_teacher_choose(msg: Message):
    kb = deepcopy(KB_SCHEDULE)
    await msg.answer("Обери:", reply_markup=kb)


async def __schedule_teacher_send1(msg: Message):
    user_id = msg.from_user.id
    if msg.text == 'На Сьогодні':
        lessonDate = get_day_date()
    else:
        lessonDate = get_next_day_date()

    status = get_status_by_id(user_id)
    teacher_id = get_teacher_id(user_id)
    id_t, f_name, m_name, l_name, status_of_subs = get_teacher_data(teacher_id)
    teacher_id = get_teacher_id_by_name_politek(f_name, m_name, l_name)

    res = get_rozklad_by_teacher(teacher_id, start_date=lessonDate, end_date=lessonDate)

    if res:
        data = json_parser(res, status)
        loguru.logger.info(f' 200 {user_id}')
        for key, value in data.items():
            value = sorted(value, key=lambda value: int(value[3:4]))
            await msg.answer(hbold(key) + ':\n' + ''.join(value))
    else:
        await msg.answer('Розкладу не знайдено.')
        return 'BAD request'


async def __schedule_teacher_send_callback_kb(msg: Message):
    kb = deepcopy(KB_SCHEDULE_WEEK)
    await msg.answer("Обери:", reply_markup=kb)


async def __schedule_teacher_week_callback(query: CallbackQuery):
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

    teacher_id = get_teacher_id(user_id)
    id_t, f_name, m_name, l_name, status_of_subs = get_teacher_data(teacher_id)
    teacher_id = get_teacher_id_by_name_politek(f_name, m_name, l_name)
    res = get_rozklad_by_teacher(teacher_id, start_date=lessonDateStart, end_date=lessonDateEnd)

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


async def __free_audience_step_1(msg: Message, state: FSMContext):
    await state.set_state(Free_audience.init_state)

    kb = deepcopy(KB_FREE_AUDIENCE)
    await msg.answer('Оберіть номер пари для пошуку вільної авдиторії.', reply_markup=kb)
    await state.set_state(Free_audience.answer_state)


async def __free_audience_step_2(msg: Message, state: FSMContext):
    kb = KB_GO_TO_MENU
    choice = [('1️⃣', '1'), ('2️⃣', '2'), ('3️⃣', '3'), ('4️⃣', '4'), ('5️⃣', '5'), ('6️⃣', '6')]
    try:
        lesson_number = [index for emoji, index in choice if emoji == msg.text][0]
    except IndexError:
        lesson_number = 1

    free_rooms = audience(lesson_number)
    for block, rooms in free_rooms.items():

        await msg.answer(f"<b>Вільні аудиторії в {block} на {lesson_number} пару:</b>"
                         f" \n\n{', '.join(rooms).replace(block + ' /','')}\n",
                         reply_markup=kb, parse_mode="HTML")
    await state.finish()


def register_teacher_handlers(dp: Dispatcher):

    dp.register_message_handler(__schedule_teacher_choose, IsTeacher(),
                                content_types=["text"], text="Розклад🗓")
    dp.register_message_handler(__schedule_teacher_send1, IsTeacher(),
                                content_types=["text"], text="На Сьогодні")
    dp.register_message_handler(__schedule_teacher_send1, IsTeacher(),
                                content_types=["text"], text="На Завтра")
    dp.register_message_handler(__schedule_teacher_send_callback_kb, IsTeacher(),
                                content_types=["text"], text="На Тиждень")
    dp.register_callback_query_handler(__schedule_teacher_week_callback, IsTeacher())
    dp.register_message_handler(__free_audience_step_1, IsTeacher(),
                                content_types=['text'], text="Пошук вільної авдиторії🔍")
    dp.register_message_handler(__free_audience_step_2, IsTeacher(),
                                content_types=['text'], state=Free_audience.answer_state)
