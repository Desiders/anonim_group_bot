from aiogram.types import Message

from ..scripts.functions import get_text


async def command_new(call: Message, database) -> None:
    room, args = await database.new_room(call.from_user.id)

    command_trigger = 'new_success' if room else 'new_warning'
    
    await call.answer(get_text(command_trigger).format(args))