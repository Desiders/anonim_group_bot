from aiogram.types import Message

from ..scripts.functions import get_text


async def command_commands(call: Message):
    await call.answer(get_text('commands'))