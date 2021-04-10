from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text


async def command_leave(call: Message, database: RedisDB):
    result, args = await database.end_room(call.from_user.id)
    if result is None:
        command_trigger = 'leave_warning'
    else:
        command_trigger = 'leave_success_and_del' if result else 'leave_success'

    await call.answer(get_text(command_trigger).format(args))
