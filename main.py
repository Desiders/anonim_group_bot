from typing import NoReturn


async def main() -> NoReturn:
    from aiogram.contrib.middlewares.logging import LoggingMiddleware

    from app import register_handlers
    from app.middlewares.database import DatabaseMiddleware
    from loader import config, dispatcher, logger
    
    logger.info("Setup middlewares")
    dispatcher.middleware.setup(LoggingMiddleware())
    dispatcher.middleware.setup(DatabaseMiddleware(host=config.redis.host,
                                                   port=config.redis.port,
                                                   password=config.redis.password,
                                                   db=config.redis.db,))

    logger.info("Register handlers")
    register_handlers(dispatcher)

    logger.warning("Starting bot")
    await dispatcher.start_polling()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
