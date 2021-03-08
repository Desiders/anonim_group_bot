from aiogram.types import Message

from ..scripts.functions import get_text


async def command_donate(call: Message):
    await call.answer(get_text('donate'))