from asyncio import create_task, get_event_loop
from typing import Dict, List, Union

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import MediaGroup, Message
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from app.services.database import RedisDB

from ..scripts.functions import get_name, get_text, time_sleep

ACCESS_TYPES = ('text',
                'audio',
                'document',
                'photo',
                'video',
                'animation',
                'voice')
IGNORE_TYPES = ('pinned_message')


def get_media_group(album: List[tuple]) -> MediaGroup:
    media_album = MediaGroup()
    for media in album:
        file_id, content_type, caption = media
        media = {'media': file_id, 'type': content_type, 'caption': caption}
        media_album.attach(media)
    return media_album


async def send_media_group(call: Message,
                           state: FSMContext,
                           database: RedisDB) -> None:
    async with state.proxy() as data:
        album = data[call.media_group_id]['album']
        users = data[call.media_group_id]['users']
        media_group = get_media_group(album)
        for user_id in users:
            await time_sleep('new_message_group')
            try:
                await call.bot.send_media_group(user_id, media_group)
            except (BotBlocked, UserDeactivated):
                await database.end_user(user_id)


async def send_media_single(call: Message,
                            caption: str,
                            users: List[str],
                            database: RedisDB) -> None:
    content_type = call.content_type
    if content_type not in ACCESS_TYPES:
        if content_type in IGNORE_TYPES:
            return None
        return await call.reply(get_text('send_warning_single'))
    type_sleep = 'new_message_single'
    if 'text' in call:
        for user_id in users:
            await time_sleep(type_sleep)
            try:
                await call.bot.send_message(user_id, caption, parse_mode='')
            except (BotBlocked, UserDeactivated):
                await database.end_user(user_id)
    else:
        from_chat_id, message_id = call.chat.id, call.message_id
        for user_id in users:
            await time_sleep(type_sleep)
            try:
                await call.bot.copy_message(user_id, from_chat_id, message_id,
                                            caption=caption, parse_mode='')
            except (BotBlocked, UserDeactivated):
                await database.end_user(user_id)


def get_caption(call: Message, author: Dict[str, str]) -> Union[bool, str]:
    if 'text' in call:
        caption = call.text
        if len(caption) > 4000:
            return False
    elif 'caption' in call:
        caption = call.caption
        if len(caption) > 900:
            return False
    else:
        caption = ''
    nickname = get_name(author)
    user_index = author['user_index']
    caption = get_text('send_message').format(nickname,
                                              user_index,
                                              caption)
    return caption


async def command_send_album(call: Message,
                             state: FSMContext,
                             database: RedisDB) -> None:
    author, users = await database.get_members_over_send(call.from_user.id)
    if not users:
        return None
    async with state.proxy() as data:
        media_group_id = call.media_group_id
        if media_group_id not in data:
            get_event_loop().call_later(0.3, create_task, send_media_group(call,
                                                                           state,
                                                                           database))
            caption = get_caption(call, author)
            if not caption:
                return await call.reply(get_text('send_warning_long'))
        else:
            caption = ''
        content_type = call.content_type
        if content_type == 'photo':
            file_id = call.photo[-1].file_id
        else:
            file_id = call[call.content_type].file_id
        del users[author["user_index"]]
        standart_values = {'album': [], 'users': users}
        media = (file_id, content_type, caption)
        data._data.setdefault(media_group_id, standart_values)['album'].append(media)


async def command_send_single(call: Message, database: RedisDB) -> None:
    author, users = await database.get_members_over_send(call.from_user.id)
    if not users:
        return None
    caption = get_caption(call, author)
    if not caption:
        return await call.reply(get_text('send_warning_long'))
    del users[author["user_index"]]
    get_event_loop().call_later(0.1, create_task, send_media_single(call,
                                                                    caption,
                                                                    users,
                                                                    database))