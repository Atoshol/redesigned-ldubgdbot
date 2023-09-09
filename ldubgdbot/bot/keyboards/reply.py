from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


KB_START_BOT: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_START_BOT.add(KeyboardButton(text="Зареєструватись"))

KB_GO_TO_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_GO_TO_MENU.add(KeyboardButton(text="Меню"))

KB_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

KB_REGISTRATION: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_REGISTRATION.add(KeyboardButton(text='Викладач👩‍🏫👨‍🏫'))
KB_REGISTRATION.add(KeyboardButton(text='Студент/Курсант👩‍🎓👨‍🎓'))
KB_REGISTRATION.add(KeyboardButton(text='Працівник'))

KB_REMOVE: Final = ReplyKeyboardRemove()

KB_SCHEDULE: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_SCHEDULE.add(KeyboardButton(text="На Сьогодні"))
KB_SCHEDULE.add(KeyboardButton(text="На Завтра"))
KB_SCHEDULE.add(KeyboardButton(text="На Тиждень"))
KB_SCHEDULE.add(KeyboardButton(text="Меню"))

KB_SUBSCRIPTION: Final = ReplyKeyboardMarkup(resize_keyboard=True)
KB_SUBSCRIPTION.add(KeyboardButton(text='Підписатись✍️'))
KB_SUBSCRIPTION.add(KeyboardButton(text='Відписатись❌'))
KB_SUBSCRIPTION.add(KeyboardButton(text='Статус підписки'))
KB_SUBSCRIPTION.add(KeyboardButton(text="Меню"))

KB_FREE_AUDIENCE: Final = ReplyKeyboardMarkup(resize_keyboard=True)
for i in [['1️⃣', '2️⃣'], ['3️⃣', '4️⃣'], ['5️⃣', '6️⃣']]:
    KB_FREE_AUDIENCE.row(KeyboardButton(f'{i[0]}'), KeyboardButton(f'{i[1]}'))

KB_SEARCH: Final = ReplyKeyboardMarkup(resize_keyboard=True)
KB_SEARCH.add(KeyboardButton(text="За викладачем"), KeyboardButton(text="За групою"))

KB_SEARCH_SKIP: Final = ReplyKeyboardMarkup(resize_keyboard=True)
KB_SEARCH_SKIP.add(KeyboardButton(text="Пропустити"))

