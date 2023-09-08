from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


KB_SCHEDULE_WEEK: Final = InlineKeyboardMarkup(row_width=3)
buttons = [
        InlineKeyboardButton(text="Понеділок", callback_data="Понеділок"),
        InlineKeyboardButton(text="Вівторок", callback_data="Вівторок"),
        InlineKeyboardButton(text="Середа", callback_data="Середа"),
        InlineKeyboardButton(text="Четвер", callback_data="Четвер"),
        InlineKeyboardButton(text="П'ятниця", callback_data="П'ятниця"),
        InlineKeyboardButton(text="Субота", callback_data="Субота"),
        InlineKeyboardButton(text="Завершити перегляд", callback_data="Завершити перегляд")
    ]
KB_SCHEDULE_WEEK.add(*buttons)

KB_INLINE_LINKS: Final = InlineKeyboardMarkup(row_width=1)
KB_INLINE_LINKS.add(InlineKeyboardButton(text='Віртуальний Університет',
                                         url='http://virt.ldubgd.edu.ua'))
KB_INLINE_LINKS.add(InlineKeyboardButton(text='Система Деканат',
                                         url='https://rozklad.ldubgd.edu.ua/cgi-bin/classman.cgi?n=999'))
KB_INLINE_LINKS.add(InlineKeyboardButton(text='Канал Тех-підтримки університету',
                                         url='https://t.me/lsuls_teams'))
KB_INLINE_LINKS.add(InlineKeyboardButton(text='Сайт університету',
                                         url='https://ldubgd.edu.ua'))
