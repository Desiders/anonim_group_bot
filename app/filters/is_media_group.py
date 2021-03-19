from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsMediaGroup(BoundFilter):
    key = "is_media_group"

    def __init__(self, is_media_group: bool):
        self.is_media_group = is_media_group

    async def check(self, call: Message) -> bool:
        return bool(call.media_group_id) is self.is_media_group
