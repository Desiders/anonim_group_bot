from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text


def register_handlers(dispatcher: Dispatcher) -> None:
    from aiogram.dispatcher.filters import CommandHelp, CommandStart
    from aiogram.types.message import ContentType

    from .change import command_change
    from .commands import command_commands
    from .donate import command_donate
    from .edit import EditCache, command_edit, join_number, join_object
    from .end import command_end
    from .get import command_get
    from .help import command_help
    from .info import command_info
    from .join import command_join
    from .kick import command_kick
    from .members import command_members
    from .new import command_new
    from .profile import command_profile
    from .room import command_room
    from .rooms import command_rooms, get_rooms
    from .start import command_start

    dispatcher.register_message_handler(command_start, CommandStart())
    dispatcher.register_message_handler(command_help, CommandHelp())
    dispatcher.register_message_handler(command_commands, commands='commands')
    dispatcher.register_message_handler(command_rooms, commands='rooms')
    dispatcher.register_callback_query_handler(get_rooms, Text(endswith='rooms'))
    dispatcher.register_message_handler(command_room, commands='room')
    dispatcher.register_message_handler(command_new, commands='new')
    dispatcher.register_message_handler(command_join, commands='join')
    dispatcher.register_message_handler(command_end, commands='end')
    dispatcher.register_message_handler(command_members, commands='members')
    dispatcher.register_message_handler(command_kick, commands='kick')
    dispatcher.register_message_handler(command_change, commands='change')
    dispatcher.register_message_handler(command_profile, commands='profile')
    dispatcher.register_message_handler(command_get, commands='get')
    dispatcher.register_message_handler(command_edit, commands='edit')
    dispatcher.register_message_handler(join_number, state=EditCache.number_object, content_types=ContentType.ANY)
    dispatcher.register_message_handler(join_object, state=EditCache.new_object, content_types=ContentType.ANY)
    dispatcher.register_message_handler(command_info, commands='info')
    dispatcher.register_message_handler(command_donate, commands='donate')
