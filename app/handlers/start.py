from aiogram.types import Message

from ..scripts.functions import get_text


async def command_start(call: Message, database) -> None:
    await call.answer(get_text('start'))
    await database.add_user(call.from_user.id)
