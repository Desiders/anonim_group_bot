from aiogram.types import Message

from ..scripts.functions import get_text


async def command_help(call: Message) -> None:
    await call.answer(get_text('help'))