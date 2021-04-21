from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text


async def command_start(call: Message, database: RedisDB):
    await call.answer(get_text('start'))

    await database.add_user(call.from_user.id)