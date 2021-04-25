from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import (
    get_description,
    get_name,
    get_photo,
    get_text,
    validate_get_user_index
)


async def command_get(call: Message, database: RedisDB) -> None:
    user_index = call.get_args()
    if not user_index:
        return await call.answer(get_text('get_no_args'))
    if not validate_get_user_index(user_index):
        return await call.answer(get_text('get_warning_no_have'))
    profile = await database.get_profile(call.from_user.id, int(user_index))
    if profile is None:
        return await call.answer(get_text('get_warning'))
    if not profile and profile != {}:
        return await call.answer(get_text('get_warning_no_have'))
    nickname = get_name(profile)
    description = get_description(profile)
    photo = get_photo(profile)
    text = get_text('get_profile').format(user_index, nickname,
                                          description)
    if photo:
        await call.answer_photo(photo=photo, caption=text,
                                parse_mode='')
    else:
        await call.answer(text, parse_mode='')