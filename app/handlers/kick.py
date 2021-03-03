import asyncio
from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, validate_input_kick_user_index
from ..services.database import MAX_LENGTH_ROOM


async def command_kick(call: Message, database) -> None:
    kick_user_id = call.get_args()
    if not kick_user_id:
        return await call.answer(get_text('kick_no_args'))

    access, text = validate_input_kick_user_index(kick_user_id, MAX_LENGTH_ROOM)
    if not access:
        if text == 'no_number' or text == 'long_id':
            command_trigger = 'kick_warning_no_have'
        else: # elif text == 'kick_admin'
            command_trigger = 'kick_warning_admin'
        return await call.answer(get_text(command_trigger).format(kick_user_id), parse_mode='')

    send = False
    user, access_or_args = await database.kick_user_over_id_from_room(call.from_user.id, int(kick_user_id))
    if not user:
        command_trigger = 'kick_warning' if user is None else 'kick_warning_no_have'
    elif not access_or_args:
        command_trigger = 'kick_warning_access'
    else:
        send = True
        command_trigger = 'kick_success'
        user_index, user_nickname, room_id, user_id, users = access_or_args
        del (users[user_index], users[0]) # Убираем из рассылки исключённого пользователя и админа
        if not user_nickname:
            user_nickname  = config.standart.standart_name

    await call.answer(get_text(command_trigger).format(access_or_args), parse_mode='')

    if send:
        await call.bot.send_message(chat_id=user_id, text=get_text('kick_notify').format(room_id))

        for user in users:
            await asyncio.sleep(config.standart.time_sleep_end_member)
            await call.bot.send_message(
                chat_id=user_id, text=get_text('kick_notify_all').format(user_index, user_nickname), parse_mode=''
            )

