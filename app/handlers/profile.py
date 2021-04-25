from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_description, get_name, get_photo, get_text


async def command_profile(call: Message, database: RedisDB) -> None:
    profile = await database.get_my_profile(call.from_user.id)
    nickname = get_name(profile)
    description = get_description(profile)
    photo = get_photo(profile)
    text = get_text('profile').format(nickname, description)
    if photo:
        await call.answer_photo(photo=photo, caption=text,
                                parse_mode='')
    else:
        await call.answer(text=text, parse_mode='')