from aiogram.types import Message

from ..scripts.functions import get_text


async def command_create(call: Message, database):
    room, args = await database.new_room(call.from_user.id)
    # Создаём комнату в случае, если пользователь не является её членом, иначе предупреждаем пользователя о наличии комнаты
    command_trigger = 'create_success' if room else 'create_warning'
    await call.answer(get_text(command_trigger).format(args))