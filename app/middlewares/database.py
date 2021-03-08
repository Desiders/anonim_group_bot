from typing import Union

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, database):
        super().__init__()
        self.database = database

    async def pre_process(self, call: Union[Message, CallbackQuery], data: dict):
        data["database"] = self.database

    async def trigger(self, action, args):
        call, *_, data = args
        if action == 'pre_process_message' or action == 'pre_process_callback_query':
            await self.pre_process(call, data)
        else:
            return False
        return True
