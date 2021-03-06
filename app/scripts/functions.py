import json
import random
from typing import List, Tuple, Union

from aiogram.types.message import Message

from .. import wording


def get_text(name: str) -> str:
    return json.loads(wording.get_texts())[name]


def generate_key(*parts: Tuple[str, int]) -> str:
    return ':'.join(tuple(map(str, parts)))


def generate_room_id(mod: bool = False) -> str:
    iterations = 4 if mod else 3
    random_numbers = (random.randrange(1, 1000) for _ in range(iterations))
    room_id = "-".join(tuple(map(str, random_numbers)))
    return room_id


def generate_key_users(type_generate: str, users: List[int]) -> List[str]:
    key_users = [generate_key(type_generate, user) for user in users]
    return key_users


def validate_input_join_room_id(room_id: str) -> bool:
    length_hyphen = room_id.count('-')
    if not (1 < length_hyphen < 4):
        return False

    without_hyphen = room_id.replace('-', '')
    if not without_hyphen.isdecimal():
        return False

    if not (1 < length_hyphen < 5):
        return False

    length_without_hyphen = len(without_hyphen)
    if length_without_hyphen > 3 + (length_hyphen * 3):
        return False

    return True


def new_object_over_type(type_object: str, input_object: Message, standart: dict) -> Union[str, None]:                    
    if type_object == 'photo':
        return input_object.photo[-1].file_id

    if type_object == 'nickname' or type_object == 'description':
        text = input_object.text
        if type_object == 'nickname':
            MIN_LENGTH = standart['min_length_nickname']
            MAX_LENGTH = standart['max_length_nickname']
        else:
            MIN_LENGTH = standart['min_length_description']
            MAX_LENGTH = standart['max_length_description']
        if MIN_LENGTH <= len(text) <= MAX_LENGTH:
            return text


def rooms_appropriate_mode(rooms: List[str], mode: str) -> List[str]:
    available_rooms = [room for room in rooms if rooms[room] == '1'] # == '1' проверка на то, активна ли группа
    length_rooms = len(available_rooms)
    if mode.startswith('random'):
        random.shuffle(available_rooms)
        return available_rooms

    iteration = length_rooms if length_rooms < 5 else 5
    if mode.startswith('new'):
        reverse_rooms = available_rooms[::-1]
        rooms = reverse_rooms[:iteration]
    else: # elif mode.startswith('old')
        rooms = available_rooms[:iteration]
    return rooms


def rooms_formatted_over_text(rooms: list) -> str:
    if rooms == []:
        return

    start = '- '
    style = '<code>{}</code>'
    rooms_formatted = [start + style.format(room) for room in rooms]
    rooms_over_text = '\n'.join(rooms_formatted)
    return rooms_over_text


def validate_input_kick_user_index(kick_user_id: str, max_users_id: int) -> Tuple[Union[bool, str]]:
    if not kick_user_id.isdecimal():
        return (False, 'no_number')

    if kick_user_id == '0':
        return (False, 'kick_admin')

    if int(kick_user_id) > max_users_id:
        return (False, 'long_id')

    return (True, ...)


def validate_input_get_user_index(user_index: str) -> bool:
    if not user_index.isdecimal():
        return False

    if not (-1 < int(user_index) < 11):
        return False

    return True


def indexes_formatted_over_text(length: int) -> str:
    style = '<b>{}</b>'
    indexes = [style.format(number) for number in range(length)]
    indexes_over_text = ', '.join(indexes)
    return indexes_over_text