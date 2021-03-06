from aiogram.types import Message

from ..scripts.functions import get_text


async def command_room(call: Message, database) -> None:
    room, args = await database.get_room(call.from_user.id)
    # Выводим информацию о комнате, если являемся её членом, иначе предупреждаем о отсутсвии комнаты
    command_trigger = 'room_success' if room else 'room_warning'
    await call.answer(get_text(command_trigger).format(args))