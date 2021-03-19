import asyncio
from typing import Dict, List, Union

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import MediaGroup, Message

from ..scripts.functions import get_name, get_text, time_sleep

ACCESS_TYPES = ['text', 'audio', 'document', 'photo', 'video', 'animation', 'voice']
IGNORE_TYPES = ['pinned_message']


def get_media_group(album: list) -> list:
    media_album = MediaGroup()
    for media in album:
        file_id, content_type, caption = media
        media = {'media': file_id, 'type': content_type, 'caption': caption}
        media_album.attach(media)
    return media_album


async def send_media_group(call: Message, state: FSMContext):
    async with state.proxy() as data:
        album, users = data[call.media_group_id]['album'], data[call.media_group_id]['users']
        media_group = get_media_group(album)
        for user_id in users:
            await time_sleep('new_message_group')
            try:
                await call.bot.send_media_group(user_id, media_group)
            except: ...


async def send_media_single(call: Message, caption: str, author: Dict[str, str], users: List[str]) -> None:
    content_type = call.content_type
    if content_type not in ACCESS_TYPES:
        if content_type in IGNORE_TYPES:
            return
        return await call.reply(get_text('send_warning_single'))
    type_sleep = 'new_message_single'
    if 'text' in call:
        for user_id in users:
            await time_sleep(type_sleep)
            try:
                await call.bot.send_message(user_id, caption, parse_mode='')
            except: ...
    else:
        from_chat_id, message_id = call.chat.id, call.message_id
        for user_id in users:
            await time_sleep(type_sleep)
            try:
                await call.bot.copy_message(user_id, from_chat_id, message_id,
                                            caption=caption, parse_mode='')
            except: ...


def get_caption(call: Message, author: Dict[str, str]) -> Union[None, str]:
    if 'text' in call:
        caption = call.text
        if len(caption) > 4000:
            return
    elif 'caption' in call:
        caption = call.caption
        if len(caption) > 900:
            return
    else:
        caption = ''
    nickname = get_name(author)
    user_index = author['user_index']
    caption = get_text('send_message').format(nickname, user_index, caption)
    return caption


async def command_send_album(call: Message, state: FSMContext, database) -> None:
    author, users = await database.get_members_over_send(call.from_user.id)
    if not users:
        return
    async with state.proxy() as data:
        if call.media_group_id not in data:
            asyncio.get_event_loop().call_later(1.5, asyncio.create_task, send_media_group(call, state))
            caption = get_caption(call, author)
            if caption is None:
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
        data._data.setdefault(call.media_group_id, standart_values)['album'].append(media)


async def command_send_single(call: Message, database) -> None:
    author, users = await database.get_members_over_send(call.from_user.id)
    if not users:
        return
    caption = get_caption(call, author)
    if caption is None:
        return await call.reply(get_text('send_warning_long'))
    del users[author["user_index"]]
    asyncio.get_event_loop().call_later(0.1, asyncio.create_task, send_media_single(call, caption,
                                                                                    author, users))
