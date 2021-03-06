from aiogram.types import Message

from ..scripts.functions import get_text


async def command_change(call: Message, database) -> None:
    result, args = await database.change_id_room(call.from_user.id)
    # Если вы не являетесь членом какой-либо комнаты
    if result is None:
        command_trigger = 'change_warning'
    # Уведомляет о успешной смене номера комнаты или о отсутствии прав администратора комнаты
    else:
        command_trigger = 'change_success' if result else 'change_warning_access'
    await call.answer(get_text(command_trigger).format(args))