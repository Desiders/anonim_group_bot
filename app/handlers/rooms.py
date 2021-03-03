from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types.callback_query import CallbackQuery

from ..scripts.functions import (get_text, rooms_appropriate_mode,
                                 rooms_formatted_over_text)


async def command_rooms(call: Message, database) -> None:
    inline_keyboards = [
        [   InlineKeyboardButton('Новые комнаты', callback_data='new_rooms'),
            InlineKeyboardButton('Старые комнаты', callback_data='old_rooms')],
        [   InlineKeyboardButton('Случайные комнаты', callback_data='random_rooms')],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)

    await call.answer(get_text('rooms_mode'), reply_markup=markup)

async def get_rooms(call: CallbackQuery, database) -> None:
    mode = call.data
    rooms = await database.get_rooms()
    rooms_mode = rooms_appropriate_mode(rooms, mode)
    rooms_for_text = rooms_formatted_over_text(rooms_mode)
    if not rooms_for_text:
        await call.message.answer(get_text('rooms_warning'))
    else:
        await call.message.answer(get_text('rooms_success').format(rooms_for_text))

    await call.answer()
