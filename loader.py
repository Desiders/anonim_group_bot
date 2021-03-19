def get_logger():
    import logging

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] - %(filename)s (%(lineno)d string): %(message)s")
    
    return logging.getLogger(__name__)


def get_config():
    from app import load_config

    return load_config("bot.ini")


def get_dispatcher(token):
    from aiogram import Bot, Dispatcher
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    from aiogram.types import ParseMode

    return Dispatcher(Bot(token=token, parse_mode=ParseMode.HTML), storage=MemoryStorage())

logger = get_logger()
config = get_config()
dispatcher = get_dispatcher(config.bot.token)
