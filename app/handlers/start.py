from aiogram.types import Message
from app.services.database import RedisDB
from loader import logger

from ..scripts.functions import get_text


async def command_start(call: Message, database: RedisDB):
    await call.answer(get_text('start'), disable_web_page_preview=True)

    logger.info(f"User: {call.from_user.id} (@{call.from_user.username})")

    await database.add_user(call.from_user.id)
