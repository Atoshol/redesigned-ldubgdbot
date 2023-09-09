import json

from ldubgdbot.bot.keyboards.util import *
from ldubgdbot.bot.keyboards.inline import KB_INLINE_LINKS
from ldubgdbot.bot.utils.env import Env
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, Bot, types
from aiogram.types import Message, InlineQuery
from ldubgdbot.bot.utils.states import *
from functions.check_teacher import check_teacher
from functions.check_student_group import check_group
from functions.get_date import *
from functions.get_politek import *
from functions.json_parser import json_parser
from functions.get_politek import get_group_id_by_name_politek
from functions.qrcode import _get_file
import loguru
from ldubgdbot.bot.database.methods.insert import *
from ldubgdbot.bot.database.methods.delete import *


async def __start(msg: Message) -> None:
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    data = get_start_keyboard(user_id)
    keyboard = data[0]
    status = data[1]
    if not status:
        await bot.send_message(
            chat_id=user_id,
            text="Вітаю! Я бот <b>Львівського державного університету безпеки "
                 "життєдіяльності.</b>\nНатисни кнопку щоб <b>зареєструватись.</b>\n<a "
                 "href='https://telegra.ph/Posіbnik-koristuvacha-dlya-Bota-LDU-BZHD-02-04"
                 "'>Посібник користувача.</a>",
            reply_markup=keyboard, disable_web_page_preview=True
        )

    else:
        await bot.send_message(
            chat_id=user_id,
            text='Вітаю! Я бот <b>Львівського державного університету безпеки життєдіяльності.</b>\n'
                 'Ти вже зареєстрований, натисни кнопку щоб розпочати роботу.',
            reply_markup=keyboard
        )


async def __menu(msg: Message):
    user_id = msg.from_user.id
    data = get_menu_keyboard(user_id)
    keyboard = data[0]
    status = data[1]
    if not status:
        keyboard = get_start_keyboard(user_id)[0]
        await msg.answer(text="Ти не зареєстрований, натисни кнопку нище щоб зареєструватись!",
                         reply_markup=keyboard)

    else:
        await msg.answer("Обери:", reply_markup=keyboard)


async def __registration_step1(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = get_registration_keyboard(user_id)
    keyboard = data[0]
    status = data[1]

    if status is None:
        await msg.answer("Обери:", reply_markup=keyboard)

    else:
        await msg.answer(
            chat_id=user_id,
            text='Ти вже зареєстрований, натисни кнопку щоб розпочати роботу.',
            reply_markup=keyboard
        )

    await state.set_state(Registration_state.CHOOSE_OF_GROUP)


async def __registration_step2(msg: Message, state: FSMContext):
    user_id = msg.from_user.id

    await state.update_data(CHOOSE_OF_STATUS=msg.text)

    kb = get_registration_keyboard(user_id)[0]
    if msg.text == "Викладач👩‍🏫👨‍🏫":
        kb = deepcopy(KB_REMOVE)
        await msg.answer(text="Напишіть своє прізвище, ім'я та по батькові.",
                         reply_markup=kb)
        await state.set_state(Registration_state.TEACHER_NAME_STATE)
    elif msg.text == "Студент/Курсант👩‍🎓👨‍🎓":
        kb = deepcopy(KB_REMOVE)
        await msg.answer(text=f'З якої ти групи?(Наприклад "КН12")\n'
                              f'{hbold("Важливо врахувати регістр букв.")}\n',
                         reply_markup=kb)

        await state.set_state(Registration_state.REG_INTO_DB)
    else:
        await msg.answer("Вкажи відповідь використовуючи кнопки!", reply_markup=kb)


async def __registration_step3(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    l_name, f_name, m_name = msg.text.split(" ")
    check_out = check_teacher(f_name, m_name, l_name)
    if check_out is not None:
        await msg.answer("Введіть пароль.")
        await state.update_data(TEACHER_NAME_STATE=[f_name, m_name, l_name])
        await state.set_state(Registration_state.REG_INTO_DB)
    else:
        kb = get_start_keyboard(user_id)[0]
        await msg.answer('Не знайдено, спробуйте ще раз.', reply_markup=kb)
        await state.finish()


async def __registration_step4(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    status = data["CHOOSE_OF_STATUS"]
    f_name = msg.from_user.first_name
    username = msg.from_user.username

    if status == "Студент/Курсант👩‍🎓👨‍🎓":
        group_name = msg.text
        check_group_data = check_group(group_name)

        if check_group_data[0]:

            data = get_group_id_by_name(group_name)
            if data is None:
                group_id = insert_group(group_name)
            else:
                group_id = get_group_id_by_name(group_name)

            student_id = insert_student(username, f_name, group_id)
            insert_user(user_id=user_id, id_s=student_id)

            await state.finish()

            loguru.logger.info(f'New student - {f_name if username is None else username} {user_id}')

            kb = deepcopy(KB_GO_TO_MENU)
            await msg.answer(text='Реєстрація успішна!\nЩоб розпочати роботу натисни кнопку',
                             reply_markup=kb)

        else:
            await msg.answer(f'Не знайдено, спробуй ввести один з наступних варіантів -'
                             f' {(", ".join(check_group_data[1]))}.')
            await state.set_state(Registration_state.REG_INTO_DB)

    elif status == "Викладач👩‍🏫👨‍🏫":
        f_name, m_name, l_name = data.get("TEACHER_NAME_STATE")
        # password = check_password if else...

        # insert into public.teacher and get teacher_id

        # insert into public.user

        loguru.logger.info(f'New teacher - {l_name} {f_name} {m_name}')

        kb = deepcopy(KB_GO_TO_MENU)
        await msg.answer(text='Реєстрація успішна!\nЩоб розпочати роботу натисни кнопку',
                         reply_markup=kb)
        await state.finish()

    else:
        kb = deepcopy(KB_START_BOT)
        await msg.answer("Щось пішло не так, спробуйте знову.", reply_markup=kb)
        await state.finish()


async def __delete_registration(msg: Message):
    user_id = msg.from_user.id
    status = get_status_by_id(user_id)
    if status == 'teacher':
        delete_teacher(user_id)
    elif status == "student":
        delete_student(user_id)
    else:
        delete_admin(user_id)

    kb = KB_START_BOT
    await msg.answer('Успішно видалено, щоб розпочати роботу знову натисни кнопку:', reply_markup=kb)


async def __useful_links(msg: Message):
    kb = deepcopy(KB_INLINE_LINKS)
    await msg.answer('Натисни щоб перейти:', reply_markup=kb)


async def __inline_handler(query: InlineQuery):
    bot: Bot = query.bot
    text = query.query or 'Назва групи'

    lessonDateStart = get_day_date()
    lessonDateEnd = get_next_day_date()
    group_name = text

    group_id = get_group_id_by_name_politek(group_name)
    res = get_rozklad_by_group(group_id, lessonDateStart, lessonDateEnd)
    day = {
        'first': hbold(get_name_of_week_by_date(lessonDateStart)),
        'second': hbold(get_name_of_week_by_date(lessonDateEnd))
    }
    status = "student"
    if res:
        data = json_parser(res, status)
        text = []
        for key, value in data.items():
            value = sorted(value, key=lambda value: int(value[3:4]))
            text.append(hbold(key) + ':\n' + ''.join(value))
    else:
        text = []

    if len(text) == 2:
        today = types.InputTextMessageContent(text[0])
        tomorrow = types.InputTextMessageContent(text[1])
        description_today = 'Знайдено'
        description_tomorrow = 'Знайдено'
    elif len(text) == 1:
        if text[0].startswith(day['first']):
            today = types.InputTextMessageContent(text[0])
            tomorrow = types.InputTextMessageContent('Занятть не знайдено.')
            description_today = 'Знайдено '
            description_tomorrow = 'Не знайдено'
        elif text[0].startswith(day['second']):
            tomorrow = types.InputTextMessageContent(text[0])
            today = types.InputTextMessageContent('Занятть не знайдено.')
            description_today = 'Не Знайдено'
            description_tomorrow = 'Знайдено'
        else:
            today = types.InputTextMessageContent('Занятть не знайдено.')
            tomorrow = types.InputTextMessageContent('Занятть не знайдено.')
            description_today = 'Не Знайдено'
            description_tomorrow = 'Не Знайдено'
    else:
        today = types.InputTextMessageContent('Занятть не знайдено.')
        tomorrow = types.InputTextMessageContent('Занятть не знайдено.')
        description_today = 'Не Знайдено'
        description_tomorrow = 'Не Знайдено'
    results = [
        types.InlineQueryResultArticle(
            id='1',
            title=f'Розклад для групи: {group_name!r} На Сьогодні',
            input_message_content=today,
            description=description_today,
            thumb_url="https://i.pinimg.com/736x/06/2d/f8/062df833fd1b91178e573fe015090fe6.jpg",

        ),
        types.InlineQueryResultArticle(
            id='2',
            title=f'Розклад для групи: {group_name!r} На Завтра',
            input_message_content=tomorrow,
            description=description_tomorrow,
            thumb_url="https://i.pinimg.com/736x/06/2d/f8/062df833fd1b91178e573fe015090fe6.jpg",
        )
    ]
    # cache_time = 1 for testing (default is 300s)
    await bot.answer_inline_query(query.id, results=results, cache_time=1)


async def __feedback_step1(msg: Message, state: FSMContext):
    kb = deepcopy(KB_REMOVE)
    await msg.answer('Опиши помилку, одним повідомленням.', reply_markup=kb)
    await state.set_state(Feedback_state.answer_state)


async def __feedback_step2(msg: Message, state: FSMContext):
    bot: Bot = msg.bot

    kb = deepcopy(KB_GO_TO_MENU)
    user_id = msg.from_user.id
    msg_id = msg.message_id
    chat_id = Env.FEEDBACK_CHAT_ID
    status = get_status_by_id(user_id)

    await bot.send_message(chat_id=chat_id, text=f"Message from {user_id} | {status}")
    await bot.forward_message(chat_id=chat_id, message_id=msg_id, from_chat_id=user_id)
    await msg.answer("Дякуємо що повідомили.", reply_markup=kb)
    await state.finish()


async def __search_step1(msg: Message, state: FSMContext):
    kb = deepcopy(KB_SEARCH)
    await msg.answer("Обери:", reply_markup=kb)
    await state.set_state(Search_state.input_data)


async def __search_step2(msg: Message, state: FSMContext):
    answer = msg.text
    kb = deepcopy(KB_REMOVE)
    await state.update_data(choose_type=answer)
    if answer == 'За викладачем':
        await msg.answer('Введи ПІБ викладача', reply_markup=kb)
        await Search_state.next()
    elif answer == 'За групою':
        await msg.answer('Введи скорочену назву групи - Наприклад "КН12".', reply_markup=kb)
        await Search_state.next()
    else:
        kb = deepcopy(KB_GO_TO_MENU)
        await msg.answer('Виникла помилка\nНатисни щоб повернутись в меню.', reply_markup=kb)
        await state.finish()


async def __search_step3(msg: Message, state: FSMContext):
    answer = msg.text
    await state.update_data(input_data=answer)
    kb = deepcopy(KB_SEARCH_SKIP)
    await msg.answer('Введи дату в форматі (від) день.місяць.рік - (до) день.місяць.рік,'
                     ' або натисни кнопку щоб пропустити цей етап.', reply_markup=kb)
    await Search_state.next()


async def __search_step4(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    status = data.get('choose_type')
    group_or_pib = data.get('input_data')
    answer = 0 if msg.text == 'Пропустити' else msg.text
    if answer:
        try:
            answer = answer.split('-')
            lessonDateStart = answer[0].replace(' ', '')
            lessonDateEnd = answer[1].replace(' ', '')
        except:
            lessonDateStart = get_day_date()
            lessonDateEnd = get_next_day_date()
            await msg.answer('Не вдалось зчитати введену дату, замінено на Сьогоднішню.')
    else:
        lessonDateStart = get_day_date()
        lessonDateEnd = get_next_day_date()

    if status == "За викладачем":
        l, f, m = group_or_pib.split(" ")
        teacher_id = get_teacher_id_by_name_politek(f, m, l)
        res = get_rozklad_by_teacher(teacher_id, lessonDateStart, lessonDateEnd)
    elif status == "За групою":
        group_id = get_group_id_by_name_politek(group_or_pib)
        res = get_rozklad_by_group(group_id, lessonDateStart, lessonDateEnd)
    else:
        kb = deepcopy(KB_GO_TO_MENU)
        await msg.answer('Щось пішло не так', reply_markup=kb)
        return ''

    status = 'teacher' if status == 'За викладачем' else 'student'
    kb = deepcopy(KB_GO_TO_MENU)

    if res:
        data = json_parser(res, status)
        loguru.logger.info(f' 200 {user_id}')
        for key, value in data.items():
            value = sorted(value, key=lambda value: int(value[3:4]))
            await msg.answer(hbold(key) + ':\n' + ''.join(value))
    else:
        await msg.answer('Розкладу не знайдено.', reply_markup=kb)
    await state.finish()

    await msg.answer("Повернутись в меню:", reply_markup=kb)


async def __qr_code_step1(msg: Message, state: FSMContext):
    kb = deepcopy(KB_REMOVE)
    await msg.answer('Надішли qrcode як фото.', reply_markup=kb)
    await state.set_state(Qr_state.answer_state)


async def __qr_code_step2(msg: Message, state: FSMContext):
    kb = deepcopy(KB_GO_TO_MENU)
    user_id = msg.from_user.id
    bot: Bot = msg.bot

    file_id = msg.photo[-1].file_id
    file_content = _get_file(file_id)
    qr_api_url = 'http://api.qrserver.com/v1/read-qr-code/'
    res = requests.post(url=qr_api_url, files={'file': file_content})
    json_res = json.loads(res.content)
    qr_data = json_res[0]["symbol"][0]['data']

    audience_id = get_room_id_by_audience(qr_data)
    res = get_rozklad_by_audience(audience_id)
    if res:
        data = json_parser(res)
        loguru.logger.info(f' 200 {user_id}')
        for key, value in data.items():
            value = sorted(value, key=lambda value: int(value[3:4]))
            await msg.answer(hbold(key) + ':\n' + ''.join(value))
    else:
        await msg.answer('Розкладу не знайдено.', reply_markup=kb)
    await state.finish()

    await msg.answer("Повернутись в меню:", reply_markup=kb)


async def __qr_code_exception(msg: Message, state: FSMContext):
    kb = deepcopy(KB_GO_TO_MENU)
    await msg.answer("Повинно бути фото, а не текст, натисни щоб повернутись в меню.", reply_markup=kb)
    await state.finish()


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(__start, commands=["start"])
    dp.register_message_handler(__menu, content_types=['text'], text="Меню")

    # registration region

    dp.register_message_handler(__registration_step1, content_types=['text'], text="Зареєструватись")
    dp.register_message_handler(__registration_step2, content_types=['text'],
                                state=Registration_state.CHOOSE_OF_GROUP)
    dp.register_message_handler(__registration_step3, content_types=['text'],
                                state=Registration_state.TEACHER_NAME_STATE)
    dp.register_message_handler(__registration_step4, content_types=['text'],
                                state=Registration_state.REG_INTO_DB)

    # end region

    dp.register_message_handler(__delete_registration, content_types=['text'], text='Видалити реєстрацію❌')

    dp.register_message_handler(__useful_links, content_types=['text'], text='Корисні посилання📚')

    dp.register_message_handler(__feedback_step1, content_types=['text'], text="Повідомити про помилку📮")
    dp.register_message_handler(__feedback_step2, content_types=['text'], state=Feedback_state.answer_state)

    dp.register_message_handler(__search_step1, content_types=['text'], text="Пошук🔍")
    dp.register_message_handler(__search_step2, content_types=['text'], state=Search_state.input_data)
    dp.register_message_handler(__search_step3, content_types=['text'], state=Search_state.input_date)
    dp.register_message_handler(__search_step4, content_types=['text'], state=Search_state.send_response)

    dp.register_message_handler(__qr_code_step1, content_types=['text'], text='Сканувати qrcode📱')
    dp.register_message_handler(__qr_code_step2, content_types=['photo'], state=Qr_state.answer_state)
    dp.register_message_handler(__qr_code_exception, content_types=['text'], state=Qr_state.answer_state)

    dp.register_inline_handler(__inline_handler)
