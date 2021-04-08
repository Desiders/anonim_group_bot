from loader import logger


async def command_error(exception):
    logger.error(f"Trigger exception: {exception}")
