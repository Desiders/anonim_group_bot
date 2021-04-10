from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text, index_formatted


async def command_members(call: Message, database: RedisDB) -> None:
    length = await database.get_members(call.from_user.id)
    if not length:
        return await call.answer(get_text('members_warning'))
    indexes = index_formatted(length)

    await call.answer(get_text('members').format(indexes))
