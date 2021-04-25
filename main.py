from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import ParseMode

from app import register_handlers
from app.middlewares.database import DatabaseMiddleware
from app.services.database import RedisDB
from loader import config


async def shutdown(dispatcher: Dispatcher) -> None:
    database: RedisDB = dispatcher.bot['database']

    await database.close()
    await database.wait_closed()


async def startup(dispatcher: Dispatcher) -> None:
    database: RedisDB = dispatcher.bot['database']

    dispatcher.middleware.setup(DatabaseMiddleware(database))

    register_handlers(dispatcher)


def main() -> None:
    database = RedisDB(host=config.redis.host,
                       port=config.redis.port,
                       password=config.redis.password,
                       db=config.redis.db)

    dispatcher = Dispatcher(storage=MemoryStorage(),
                            bot=Bot(token=config.bot.token, parse_mode=ParseMode.HTML))
    dispatcher.bot['database'] = database

    executor.start_polling(dispatcher, on_startup=startup, on_shutdown=shutdown)


if __name__ == '__main__':
    main()