from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from loader import config

from ..scripts.functions import get_text, new_object_over_type

MATCHES_NUMBERS = {
    '1': dict(type_object='nickname', type_object_for_text='никнейма', acceptable_type_object='text'),
    '2': dict(type_object='description', type_object_for_text='описания', acceptable_type_object='text'),
    '3': dict(type_object='photo', type_object_for_text='фотографии', acceptable_type_object='photo'),
}


class EditCache(StatesGroup):
    number_object = State()
    type_object = State()
    type_object_for_text = State()
    acceptable_type_objects = State()
    new_object = State()


async def command_edit(call: Message, state: FSMContext):
    await call.answer(get_text('edit'))
    await state.set_state(EditCache.number_object.state)


async def join_number(call: Message, state: FSMContext) -> None:
    number_object = call.text
    information = MATCHES_NUMBERS.get(number_object)
    # Передан некорректный аргумент в качестве номера объекта
    if not information:
        return await no_correct_object(call, state, 'edit_number_warning', number_object)

    type_object = information['type_object']
    type_object_for_text = information['type_object_for_text']
    acceptable_type_object = information['acceptable_type_object']
    async with state.proxy() as data:
        data['type_object'] = type_object
        data['type_object_for_text'] = type_object_for_text
        data['acceptable_type_object'] = acceptable_type_object
    await call.answer(get_text('edit_number_success').format(type_object_for_text))
    await state.set_state(EditCache.new_object)


async def join_object(call: Message, state: FSMContext, database) -> None:
    information = await state.get_data()
    acceptable_type_objects = information['acceptable_type_object']
    type_object_for_text = information['type_object_for_text']
    # Если для объекта передан некорректный тип данных
    if call.content_type != acceptable_type_objects:
        return await no_correct_object(call, state, 'edit_object_warning', type_object_for_text)

    type_object = information['type_object']
    standart = dict(
        min_length_nickname=config.standart.min_length_nickname,
        max_length_nickname=config.standart.max_length_nickname,
        min_length_description=config.standart.min_length_description,
        max_length_description=config.standart.max_length_description,
    )
    new_object = new_object_over_type(type_object, call, standart)
    # Если аргумент передан неправильно
    if not new_object:
        arguments = tuple(standart.values())
        return await no_correct_object(call, state, 'edit_object_restriction_warning', arguments)

    await state.finish()
    await database.edit_profile(call.from_user.id, type_object, new_object)
    await call.reply(get_text('edit_object_success'))


async def no_correct_object(call: Message, state: FSMContext, command: str, arguments: str) -> None:
    await state.finish()
    await call.reply(get_text(command).format(arguments))
