from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, validate_input_get_user_index


async def command_get(call: Message, database) -> None:
    user_index = call.get_args()
    if not user_index:
        return await call.answer(get_text('get_no_args'))
    
    if not validate_input_get_user_index(user_index):
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    user_profile = await database.get_profile(call.from_user.id, int(user_index))
    if user_profile is None:
        return await call.answer(get_text('get_warning'))

    if not user_profile and user_profile != {}:
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    nickname = user_profile.get('nickname', config.standart.standart_name)
    description = user_profile.get('description', config.standart.standart_description)
    photo = user_profile.get('photo')
    chat_id = call.chat.id
    text = get_text('get_profile').format(user_index,nickname, description)
    if photo:
        await call.bot.send_photo(chat_id=chat_id, photo=photo, 
                                  caption=text, parse_mode='')
    else:
        await call.bot.send_message(chat_id=chat_id, text=text,
                                    disable_web_page_preview=True, parse_mode='')
