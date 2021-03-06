from aiogram.types import Message

from ..scripts.functions import get_text


async def command_end(call: Message, database) -> None:
    result, args = await database.end_room(call.from_user.id)
    # Если не являетесь членом какой-либо комнаты
    if result is None:
        command_trigger = 'end_warning'
    # Уведомляет о том, что комната была удалена, если вы последний участник, иначе о том, что вы вышли из комнаты
    else:
        command_trigger = 'end_success_and_del' if result else 'end_success'
    await call.answer(get_text(command_trigger).format(args))