from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text


async def command_create(call: Message, database: RedisDB) -> None:
    room, args = await database.create_room(call.from_user.id)
    command_trigger = 'create_success' if room else 'create_warning'

    await call.answer(get_text(command_trigger).format(args))