from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text


async def command_profile(call: Message, database):
    user_profile = await database.get_my_profile(call.from_user.id)
    # Получаем никнейм пользователя из профиля, если отсутствует - устанавливаем стандартный
    nickname = user_profile.get('nickname', config.standart.standart_name)
    # Получаем описание пользователя из профиля, если отсутствует - устанавливаем стандартный
    description = user_profile.get('description', config.standart.standart_description)
    # Получаем фотографию пользователя из профиля, иначе ничего не прикрепляем
    photo = user_profile.get('photo')
    chat_id = call.chat.id
    text = get_text('profile').format(nickname, description)
    # Отправляем сообщение, если фотография присутствует в профиле
    if photo:
        await call.bot.send_photo(
            chat_id=chat_id, photo=photo, caption=text, parse_mode=''
        )
    # Отправляем сообщение, если фотография отсутствует в профиле
    else:
        await call.bot.send_message(
            chat_id=chat_id, text=text, disable_web_page_preview=True, parse_mode=''
        )
