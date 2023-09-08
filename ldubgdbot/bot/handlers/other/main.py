from ldubgdbot.bot.keyboards.util import *
from ldubgdbot.bot.keyboards.inline import KB_INLINE_LINKS
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from ldubgdbot.bot.utils.states import *
from functions.check_teacher import check_teacher
from functions.check_student_group import check_group
import loguru
from ldubgdbot.bot.database.methods.get import *
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

    dp.register_message_handler(__delete_registration, content_types=['text'], text='Видалити реєстрацію❌')

    dp.register_message_handler(__useful_links, content_types=['text'], text='Корисні посилання📚')
