from aiogram.types import Message

from ..scripts.functions import get_text, rooms_active_and_inactive


async def command_info(call: Message, database):
    server, rooms, users_count = await database.get_info()
    rooms_count = rooms_active_and_inactive(rooms)

    await call.answer(get_text('info').format(server, rooms_count, users_count))