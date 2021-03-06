import asyncio
from typing import List

from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, validate_input_kick_user_index
from ..services.database import MAX_LENGTH_ROOM


async def notify_users(call: Message, access_or_args: list):
    user_index, user_nickname, room_id, user_id, users = access_or_args
    # Убираем из рассылки исключённого пользователя и админа
    del (users[user_index], users[0])
    # Получаем никнейм пользователя из профиля, если отсутствует - устанавливаем стандартный
    if not user_nickname:
        user_nickname  = config.standart.standart_name
    await call.bot.send_message(user_id, get_text('kick_notify').format(room_id), disable_web_page_preview=True)
    for user_id in users:
        await asyncio.sleep(config.standart.time_sleep_end_member)
        await call.bot.send_message(
            user_id, get_text('kick_notify_all').format(user_index, user_nickname),
            disable_web_page_preview=True, parse_mode=''
        )


async def command_kick(call: Message, database) -> None:
    kick_user_id = call.get_args()
    # Предупреждаем участника о том, что после команды должен следовать номер участника для исключения
    if not kick_user_id:
        return await call.answer(get_text('kick_no_args'))

    access, text = validate_input_kick_user_index(kick_user_id, MAX_LENGTH_ROOM)
    # Если аргумент передан неправильно
    if not access:
        # Если номер участника для исключения является строкой или слишком длинным
        if text == 'no_number' or text == 'long_id':
            command_trigger = 'kick_warning_no_have'
        # Если номер участника для исключения является идентификатором администратора комнаты (0)
        else: # elif text == 'kick_admin'
            command_trigger = 'kick_warning_admin'
        return await call.answer(get_text(command_trigger).format(kick_user_id), parse_mode='')

    user, access_or_args = await database.kick_user_over_id_from_room(call.from_user.id, int(kick_user_id))
    # Если пользователь не является членом какой-либо комнате или исключаемый участник отсутствует в комнате
    if not user:
        command_trigger = 'kick_warning' if user is None else 'kick_warning_no_have'
    # Если у пользователя недостаточно прав для исключения пользователей
    elif not access_or_args:
        command_trigger = 'kick_warning_access'
    # Если участник был успешно исключён
    else:
        command_trigger = 'kick_success'
        asyncio.get_event_loop().call_later(0.2, asyncio.create_task, notify_users(call, access_or_args))
    await call.answer(
        get_text(command_trigger).format(access_or_args), disable_web_page_preview=True, parse_mode=''
    )

