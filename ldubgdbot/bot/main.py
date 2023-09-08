from loguru import logger

from aiogram import Bot, Dispatcher, executor
from ldubgdbot.bot.utils.env import Env
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from ldubgdbot.bot.handlers.main import register_all_handlers


def __on_start_up(dp: Dispatcher) -> None:
    logger.info('Bot starts')

    register_all_handlers(dp)


def start_telegram_bot() -> None:
    bot = Bot(token=Env.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up(dp))

