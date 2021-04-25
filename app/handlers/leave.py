from asyncio import create_task, get_event_loop

from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from app.services.database import RedisDB

from ..scripts.functions import get_name, get_text, time_sleep


async def notify_users(call: Message,
                       args: list,
                       database: RedisDB) -> None:
    user_index, user_nickname, room_id, users = args
    del users[user_index]
    for user_id in users:
        await time_sleep('leave_member')
        text = get_text('leave_notify_all').format(user_index, user_nickname)
        try:
            await call.bot.send_message(chat_id=user_id, text=text,
                                        parse_mode='')
        except (BotBlocked, UserDeactivated):
            await database.end_user(user_id, room_id)


async def command_leave(call: Message, database: RedisDB):
    room, parts = await database.leave_room(call.from_user.id)
    if room is None:
        command_trigger = 'leave_warning'
    else:
        delete = room
        if delete:
            command_trigger = 'leave_success_and_del'
        else:
            command_trigger = 'leave_success'
            nickname = parts[1]
            if not nickname:
                parts[1] = get_name()
            get_event_loop().call_later(0.2, create_task, notify_users(call, parts,
                                                                       database))
        room_id = parts[2]
        parts = room_id

    await call.answer(get_text(command_trigger).format(parts))