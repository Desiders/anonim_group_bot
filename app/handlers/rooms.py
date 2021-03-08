from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types.callback_query import CallbackQuery

from ..scripts.functions import get_text, rooms_formatted, rooms_sorted


async def command_rooms(call: Message, database):
    inline_keyboards = [
        [   InlineKeyboardButton('Новые комнаты', callback_data='new_rooms'),
            InlineKeyboardButton('Старые комнаты', callback_data='old_rooms')],
        [   InlineKeyboardButton('Случайные комнаты', callback_data='random_rooms')],
    ]
    # Создаём клавиатуру для сообщения
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)

    await call.answer(get_text('rooms_mode'), reply_markup=markup)


async def get_rooms(call: CallbackQuery, database):
    mode = call.data
    if mode.startswith('old'):
        rooms = await database.get_rooms(True)
    else:
        rooms = await database.get_rooms(False)
    random = mode.startswith('random')
    rooms_mode = rooms_sorted(rooms, random)
    rooms_for_text = rooms_formatted(rooms_mode)
    if not rooms_for_text:
        await call.message.answer(get_text('rooms_warning'))
    else:
        await call.message.answer(get_text('rooms_success').format(rooms_for_text))

    await call.answer()
