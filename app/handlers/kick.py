from asyncio import create_task, get_event_loop

from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from app.services.database import RedisDB

from ..scripts.functions import (get_name, get_text, time_sleep,
                                 validate_kick_user_index)
from ..services.database import MAX_LENGTH_ROOM


async def notify_users(call: Message,
                       access_or_args: list,
                       database: RedisDB) -> None:
    user_index, user_nickname, room_id, user_id, users = access_or_args
    del (users[user_index], users[0])
    text = get_text('kick_notify').format(room_id)
    try:
        await call.bot.send_message(chat_id=user_id, text=text)
    except (BotBlocked, UserDeactivated):
        await database.end_user(user_id, room_id)
    for user_id in users:
        await time_sleep('kick_member')
        text = get_text('kick_notify_all').format(user_index, user_nickname)
        try:
            await call.bot.send_message(chat_id=user_id, text=text,
                                        parse_mode='')
        except (BotBlocked, UserDeactivated):
            await database.end_user(user_id, room_id)


async def command_kick(call: Message,
                       database: RedisDB) -> None:
    kick_user_id = call.get_args()
    if not kick_user_id:
        return await call.answer(get_text('kick_no_args'))
    access, text = validate_kick_user_index(kick_user_id, MAX_LENGTH_ROOM)
    if not access:
        if text == 'no_number' or text == 'long_id':
            command_trigger = 'kick_warning_no_have'
        else: # elif text == 'kick_admin'
            command_trigger = 'kick_warning_admin'
        return await call.answer(get_text(command_trigger).format(kick_user_id), parse_mode='')
    user, parts = await database.kick_user(call.from_user.id, int(kick_user_id))
    if not user:
        command_trigger = 'kick_warning' if user is None else 'kick_warning_no_have'
    elif not parts:
        command_trigger = 'kick_warning_access'
    else:
        command_trigger = 'kick_success'
        nickname = parts[1]
        if not nickname:
            parts[1] = get_name()
        get_event_loop().call_later(0.2, create_task, notify_users(call, parts,
                                                                   database))

    await call.answer(get_text(command_trigger).format(parts))