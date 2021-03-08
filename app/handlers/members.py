from aiogram.types import Message

from ..scripts.functions import get_text, indexes_formatted_over_text


async def command_members(call: Message, database) -> None:
    length = await database.get_members(call.from_user.id)
    if not length:
        return await call.answer(get_text('members_warning'))
    
    indexes = indexes_formatted_over_text(length)

    await call.answer(get_text('members').format(indexes))
