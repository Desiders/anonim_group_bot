import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from app import load_config

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] - %(filename)s (%(lineno)d string): %(message)s")

config = load_config("bot.ini")

dispatcher = Dispatcher(Bot(token=config.bot.token,
                        parse_mode=ParseMode.HTML),
                        storage=MemoryStorage())
