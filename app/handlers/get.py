from aiogram.types import Message

from ..scripts.functions import (get_description, get_name, get_photo,
                                 get_text, validate_get_user_index)


async def command_get(call: Message, database) -> None:
    user_index = call.get_args()
    if not user_index:
        return await call.answer(get_text('get_no_args'))
    
    if not validate_get_user_index(user_index):
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    profile = await database.get_profile(call.from_user.id, int(user_index))
    if profile is None:
        return await call.answer(get_text('get_warning'))

    if not profile and profile != {}:
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    nickname = get_name(profile)
    description = get_description(profile)
    photo = get_photo(profile)
    chat_id = call.chat.id
    text = get_text('get_profile').format(user_index,nickname, description)
    if photo:
        await call.bot.send_photo(chat_id=chat_id, photo=photo, 
                                  caption=text, parse_mode='')
    else:
        await call.bot.send_message(chat_id=chat_id, text=text,
                                    disable_web_page_preview=True, parse_mode='')
