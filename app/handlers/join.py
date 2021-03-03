import asyncio

from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, validate_input_join_room_id


async def command_join(call: Message, database) -> None:
    join_id_room = call.get_args()
    if not join_id_room:
        return await call.answer(get_text('join_no_args'))

    if not validate_input_join_room_id(join_id_room):
        return await call.answer(get_text('join_warning').format(join_id_room))

    result, args = await database.join_room(call.from_user.id, join_id_room)
    if result is None:
        command_trigger = 'join_warning'
    else:
        command_trigger = 'join_success' if result else 'join_warning_have_room'

    await call.answer(get_text(command_trigger).format(args))
    if isinstance(args, tuple):
        _, user_profile, users_id = args
        nickname = user_profile.get('nickname', config.standart.standart_name)
        description = user_profile.get('description', config.standart.standart_description)
        photo = user_profile.get('photo')
        text = get_text('join_new_user').format(nickname, description)
        for user_id in users_id:
            await asyncio.sleep(config.standart.time_sleep_new_member)
            if photo:
                await call.bot.send_photo(
                    chat_id=user_id,  photo=photo, caption=text, parse_mode=''
                )
            else:
                await call.bot.send_message(
                    chat_id=user_id, text=text, disable_web_page_preview=True, parse_mode=''
                )
