from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, validate_input_get_user_index


async def command_get(call: Message, database) -> None:
    user_index = call.get_args()
    # Предупреждаем участника о том, что после команды должен следовать номер участника для просмотра профиля
    if not user_index:
        return await call.answer(get_text('get_no_args'))
    
    # Если аргументы переданы неправильно
    if not validate_input_get_user_index(user_index):
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    user_profile = await database.get_profile(call.from_user.id, int(user_index))
    # Если вы не являетесь членом какой-либо комнаты
    if user_profile is None:
        return await call.answer(get_text('get_warning'))

    # Если пользователь под указанным временным номером отсутствует в комнате
    if not user_profile and user_profile != {}:
        return await call.answer(get_text('get_warning_no_have').format(user_index))

    # Получаем никнейм пользователя из профиля, если отсутствует - устанавливаем стандартный
    nickname = user_profile.get('nickname', config.standart.standart_name)
    # Получаем описание пользователя из профиля, если отсутствует - устанавливаем стандартный
    description = user_profile.get('description', config.standart.standart_description)
    # Получаем фотографию пользователя из профиля, иначе ничего не прикрепляем
    photo = user_profile.get('photo')
    chat_id = call.chat.id
    text = get_text('get_profile').format(user_index,nickname, description)
    # Отправляем сообщение, если фотография присутствует в профиле
    if photo:
        await call.bot.send_photo(chat_id=chat_id, photo=photo, 
                                  caption=text, parse_mode='')
    # Отправляем сообщение, если фотография отсутствует в профиле
    else:
        await call.bot.send_message(chat_id=chat_id, text=text,
                                    disable_web_page_preview=True, parse_mode='')
