from aiogram.types import Message

from ..scripts.functions import get_description, get_name, get_photo, get_text


async def command_profile(call: Message, database):
    profile = await database.get_my_profile(call.from_user.id)
    nickname = get_name(profile)
    description = get_description(profile)
    photo = get_photo(profile)
    chat_id = call.chat.id
    text = get_text('profile').format(nickname, description)
    if photo:
        await call.bot.send_photo(chat_id=chat_id, photo=photo,
                                  caption=text, parse_mode='')
    else:
        await call.bot.send_message(chat_id=chat_id, text=text,
                                    disable_web_page_preview=True, parse_mode='')
