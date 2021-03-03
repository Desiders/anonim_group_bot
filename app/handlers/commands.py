from aiogram.types import Message

from ..scripts.functions import get_text


async def command_commands(call: Message) -> None:
    await call.answer(get_text('commands'))