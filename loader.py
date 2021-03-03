import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app import load_config

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(filename)s (%(lineno)d string): %(message)s",
)

config = load_config("bot.ini")

dispatcher = Dispatcher(Bot(token=config.bot.token, parse_mode=types.ParseMode.HTML), storage=MemoryStorage())
