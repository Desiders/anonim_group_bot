from typing import NoReturn


async def main() -> NoReturn:
    # from aiogram.contrib.middlewares.logging import LoggingMiddleware
    from app import register_handlers
    from app.middlewares.database import DatabaseMiddleware
    from app.services.database import RedisDB
    from loader import config, dispatcher, logger

    logger.info("Setup RedisDB")
    database = RedisDB(host=config.redis.host,
                       port=config.redis.port,
                       password=config.redis.password,
                       db=config.redis.db)

    logger.info("Setup Middleware")
    dispatcher.middleware.setup(DatabaseMiddleware(database))
    # dispatcher.middleware.setup(LoggingMiddleware(logger))

    logger.info("Register Handlers")
    register_handlers(dispatcher)

    logger.warning("Starting Bot")
    try:
        await dispatcher.start_polling()
    finally:
        await database.close()
        await database.wait_closed()
        await dispatcher.bot.session.close()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
