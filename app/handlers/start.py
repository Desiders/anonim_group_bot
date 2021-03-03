from aiogram.types import Message

from ..scripts.functions import get_text


async def command_start(call: Message) -> dict:
    await call.answer(get_text('start'))
