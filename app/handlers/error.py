from aiogram.types.update import Update
from loader import logger


async def command_error(update: Update, exception):
    logger.error(f"Trigger exception: {exception}")
    return True
