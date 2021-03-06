from typing import Union

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery

from ..services.database import RedisDB


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, host: str, port: int, password: str, db: int) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._password = password
        self._db = db

    async def pre_process(self, call: Union[Message, CallbackQuery], data: dict):
        data["database"] = RedisDB(
            host=self._host,
            port=self._port,
            password=self._password,
            db=self._db,
        )
    
    async def post_process(self, call: Union[Message, CallbackQuery], data: dict):
        database = data["database"]
        await database.close()
        await database.wait_closed()
    
    async def trigger(self, action, args):
        call, *_, data = args
        if action == 'pre_process_message' or action == 'pre_process_callback_query':
            await self.pre_process(call, data)
        elif action == 'post_process_message' or action == 'post_process_callback_query':
            await self.post_process(call, data)
        else:
            return False
        return True
