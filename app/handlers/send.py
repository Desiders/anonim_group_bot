import asyncio
from typing import Dict, List, Union

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import MediaGroup, Message
from aiogram.types.input_media import (InputMediaAudio, InputMediaDocument,
                                       InputMediaPhoto, InputMediaVideo)

from ..scripts.functions import get_name, get_text, time_sleep


def get_album(album: list) -> list:
    media_album = MediaGroup()
    for media in album:
        media_album.attach(media)

    return media_album


async def send_media_group(call: Message, state: FSMContext):
    async with state.proxy() as data:
        media, users = data[call.media_group_id]['media'], data[call.media_group_id]['users']
        media_group = get_album(media)
        for user_id in users:
            await time_sleep('new_message_group')
            try:
                await call.bot.send_media_group(user_id, media_group)
            except: ...


async def send_media_single(call: Message, caption: str, author: Dict[str, str], users: List[str]) -> None:
    content_type = call.content_type
    access_content_types = ['text', 'audio', 'document', 'photo', 'video', 'animation', 'voice']
    ignore_content_types = ['pinned_message']
    if content_type not in access_content_types:
        if content_type in ignore_content_types:
            return
        return await call.reply(get_text('send_warning'))
    if content_type == 'text':
        for user_id in users:
            await time_sleep('new_message_single')
            try:
                await call.bot.send_message(user_id, caption, parse_mode='')
            except: ...
    else:
        from_chat_id, message_id = call.chat.id, call.message_id
        for user_id in users:
            await time_sleep('new_message_single')
            try:
                await call.bot.copy_message(user_id, from_chat_id, message_id,
                                            caption=caption, parse_mode='')
            except: ...


def get_media_for_album(call: Message, caption: str) -> Union[None, object]:
    content_type = call.content_type
    if content_type == 'photo':
        photo = call.photo[-1].file_id
        media = InputMediaPhoto(media=photo, caption=caption, parse_mode='')
    elif content_type == 'video':
        video = call.video.file_id
        width = call.video.width
        height = call.video.height
        duration = call.video.duration
        media = InputMediaVideo(media=video, caption=caption, width=width,
                                height=height, duration=duration, parse_mode='')
    elif content_type == 'document':
        document = call.document.file_id
        media = InputMediaDocument(media=document, caption=caption, parse_mode='')
    elif content_type == 'audio':
        audio = call.audio.file_id
        duration = call.audio.duration
        performer = call.audio.performer
        title = call.audio.file_name
        media = InputMediaAudio(media=audio, caption=caption, duration=duration,
                                performer=performer, title=title, parse_mode='')
    else:
        return

    return media


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


async def command_send(call: Message, state: FSMContext, database) -> None:
    author, users = await database.get_members_over_send(call.from_user.id)
    if users is None:
        return

    if not users:
        return await call.reply(get_text('send_warning_no_have'))

    caption = get_caption(call, author)
    if caption is None:
        return await call.reply(get_text('send_warning_long'))

    del users[author["user_index"]]
    if 'media_group_id' in call:
        async with state.proxy() as data:
            if call.media_group_id not in data:
                asyncio.get_event_loop().call_later(1.5, asyncio.create_task, send_media_group(call, state))
            else:
                caption = ''
            media = get_media_for_album(call, caption)
            if not media:
                return await call.answer(get_text('send_warning_group'))

            standart_values = {'media': [], 'users': users}
            data._data.setdefault(call.media_group_id, standart_values)['media'].append(media)
    else:
        asyncio.get_event_loop().call_later(0.1, asyncio.create_task, send_media_single(call, caption,
                                                                                        author, users))
