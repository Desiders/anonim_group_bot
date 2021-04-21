from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types.callback_query import CallbackQuery
from app.services.database import RedisDB

from ..scripts.functions import get_text, rooms_formatted, rooms_sorted


async def command_rooms(call: Message) -> None:
    inline_keyboards = [
        [   InlineKeyboardButton('Новые комнаты', callback_data='new_rooms'),
            InlineKeyboardButton('Старые комнаты', callback_data='old_rooms')],
        [   InlineKeyboardButton('Случайные комнаты', callback_data='random_rooms')],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)

    await call.answer(get_text('rooms_mode'), reply_markup=markup)


async def get_rooms(call: CallbackQuery,
                    database: RedisDB) -> None:
    mode = call.data
    rooms = await database.get_rooms()
    use_random = mode.startswith('random')
    reverse = not mode.startswith('old')
    rooms_mode = rooms_sorted(rooms, use_random, reverse)
    rooms_for_text = rooms_formatted(rooms_mode)
    if not rooms_for_text:
        await call.message.answer(get_text('rooms_warning'))
    else:
        await call.message.answer(get_text('rooms_success').format(rooms_for_text))

    await call.answer()