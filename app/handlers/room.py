from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text


async def command_room(call: Message, database: RedisDB) -> None:
    room, args = await database.get_room(call.from_user.id)
    command_trigger = 'room_success' if room else 'room_warning'
    
    await call.answer(get_text(command_trigger).format(args))