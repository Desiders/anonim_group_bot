from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
    
    async def pre_process(self, call: Union[Message, CallbackQuery], data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        else:
            limit = self.rate_limit
            key = self.prefix + '_message'
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:
            await self.throttled(call, throttled)
            raise CancelHandler()
    
    async def throttled(self, call: Union[Message, CallbackQuery], throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await call.answer('Слишком частые запросы!')
    
    async def trigger(self, action, args):
        call, *_, data = args
        if action == 'pre_process_message' or action == 'pre_process_callback_query':
            await self.pre_process(call, data)
        else:
            return False
        return True
