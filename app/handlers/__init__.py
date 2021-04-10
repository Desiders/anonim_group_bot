from aiogram import Dispatcher


def register_handlers(dispatcher: Dispatcher):
    from aiogram.dispatcher.filters import (CommandHelp, CommandStart,
                                            MediaGroupFilter, Text)
    from aiogram.types.message import ContentType

    from .change import command_change
    from .commands import command_commands
    from .create import command_create
    from .edit import EditCache, command_edit, join_number, join_object
    from .error import command_error
    from .get import command_get
    from .help import command_help
    from .info import command_info
    from .join import command_join
    from .kick import command_kick
    from .leave import command_leave
    from .members import command_members
    from .profile import command_profile
    from .room import command_room
    from .rooms import command_rooms, get_rooms
    from .send import command_send_album, command_send_single
    from .start import command_start

    dispatcher.register_message_handler(command_start, CommandStart())
    dispatcher.register_message_handler(command_help, CommandHelp())
    dispatcher.register_message_handler(command_commands, commands=['commands', 'команды'])
    dispatcher.register_message_handler(command_rooms, commands=['rooms', 'комнаты'])
    dispatcher.register_callback_query_handler(get_rooms, Text(endswith='rooms'))
    dispatcher.register_message_handler(command_room, commands=['room', 'комната'])
    dispatcher.register_message_handler(command_create, commands=['create', 'создать'])
    dispatcher.register_message_handler(command_join, commands=['join', 'присоединиться', 'вступить'])
    dispatcher.register_message_handler(command_leave, commands=['leave', 'покинуть'])
    dispatcher.register_message_handler(command_members, commands=['members', 'участники', 'члены'])
    dispatcher.register_message_handler(command_kick, commands=['kick', 'исключить'])
    dispatcher.register_message_handler(command_change, commands=['change', 'поменять'])
    dispatcher.register_message_handler(command_get, commands=['get', 'получить'])
    dispatcher.register_message_handler(command_profile, commands=['profile', 'профиль'])
    dispatcher.register_message_handler(command_edit, commands=['edit', 'изменить'])
    dispatcher.register_message_handler(join_number,
                                        state=EditCache.number_object,
                                        content_types=ContentType.ANY)
    dispatcher.register_message_handler(join_object,
                                        state=EditCache.new_object,
                                        content_types=ContentType.ANY)
    dispatcher.register_message_handler(command_info, commands=['info', 'информация'])
    dispatcher.register_message_handler(command_send_album,
                                        MediaGroupFilter(is_media_group=True),
                                        content_types=ContentType.ANY)
    dispatcher.register_message_handler(command_send_single, content_types=ContentType.ANY)
    dispatcher.register_errors_handler(command_error)