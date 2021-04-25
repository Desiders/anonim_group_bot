from asyncio import create_task, get_event_loop
from typing import Dict, List, Tuple

from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from app.services.database import RedisDB

from ..scripts.functions import (get_description, get_name, get_photo,
                                 get_text, time_sleep, validate_room_id)


async def notify_users(call: Message,
                       args: Tuple[str, Dict[str, str], List[str]],
                       database: RedisDB) -> None:
    _, profile, users = args
    nickname = get_name(profile)
    description = get_description(profile)
    photo = get_photo(profile)
    text = get_text('join_new_user').format(nickname, description)
    if photo:
        for user_id in users:
            await time_sleep('new_member')
            try:
                await call.bot.send_photo(chat_id=user_id, photo=photo,
                                          caption=text, parse_mode='')
            except (BotBlocked, UserDeactivated):
                await database.end_user(user_id)
    else:
        for user_id in users:
            await time_sleep('new_member')
            try:
                await call.bot.send_message(chat_id=user_id, text=text,
                                            parse_mode='')
            except (BotBlocked, UserDeactivated):
                await database.end_user(user_id)


async def command_join(call: Message, database: RedisDB) -> None:
    join_id_room = (call.get_args()).replace(' ', '')
    if not join_id_room:
        return await call.answer(get_text('join_no_args'))
    if not validate_room_id(join_id_room):
        return await call.answer(get_text('join_warning'))
    result, args = await database.join_room(call.from_user.id, join_id_room)
    if result is None:
        command_trigger = 'join_warning'
    else:
        command_trigger = 'join_success' if result else 'join_warning_have_room'
    if isinstance(args, tuple):
        get_event_loop().call_later(0.2, create_task, notify_users(call, args,
                                                                   database))

    await call.answer(get_text(command_trigger).format(args))