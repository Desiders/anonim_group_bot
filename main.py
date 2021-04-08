from aiogram.dispatcher.dispatcher import Dispatcher
from app.services.database import RedisDB
from loader import config, dispatcher, logger

database = RedisDB(host=config.redis.host,
                   port=config.redis.port,
                   password=config.redis.password,
                   db=config.redis.db)


async def shutdown(dispatcher: Dispatcher):
    logger.info("Close connections")

    await database.close()
    await database.wait_closed()


async def startup(dispatcher: Dispatcher):
    from app import register_handlers
    from app.filters import setup_filters
    from app.middlewares.database import DatabaseMiddleware

    dispatcher.middleware.setup(DatabaseMiddleware(database))

    setup_filters(dispatcher)
    register_handlers(dispatcher)


def main():
    from aiogram import executor

    executor.start_polling(dispatcher,
                           skip_updates=False,
                           on_startup=startup,
                           on_shutdown=shutdown)


if __name__ == '__main__':
    main()
