import asyncio
import json
import random
from typing import List, Tuple, Union

from aiogram.types.message import Message
from loader import config

TIME_SLEEP_BY_TYPE = {'new_message_single': config.standart.time_sleep_new_message_single,
                      'new_message_group': config.standart.time_sleep_new_message_group,
                      'new_member': config.standart.time_sleep_new_member,
                      'end_member': config.standart.time_sleep_end_member}


def get_text(command: str) -> str:
    with open(f'app/wording/commands.json', encoding='utf-8') as commands:
        commands = json.load(commands)
        command = commands[command]
        return command


def generate_key(*parts: Tuple[str, int]) -> str:
    key = ':'.join(tuple(map(str, parts)))
    return key


def generate_room_id(mod: bool = False) -> str:
    iterations = 4 if mod else 3
    random_numbers = (random.randrange(1, 1000) for _ in range(iterations))
    room_id = "-".join(tuple(map(str, random_numbers)))
    return room_id


def generate_key_users(type_generate: str, users: List[int]) -> List[str]:
    key_users = [generate_key(type_generate, user) for user in users]
    return key_users


def validate_room_id(room_id: str) -> bool:
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


def validate_object(input_object: Message, type_object: str) -> Union[str, None]:                    
    if type_object == 'photo':
        return input_object.photo[-1].file_id
    if type_object == 'nickname' or type_object == 'description':
        text = input_object.text
        if type_object == 'nickname':
            min_lenght = config.standart.min_length_nickname
            max_lenght = config.standart.max_length_nickname
        else:
            min_lenght = config.standart.min_length_description
            max_lenght = config.standart.max_length_description
        if min_lenght <= len(text) <= max_lenght:
            return text
    arguments = [config.standart.min_length_nickname,
                 config.standart.max_length_nickname,
                 config.standart.min_length_description,
                 config.standart.max_length_description]
    return arguments


def rooms_sorted(rooms: List[str], random_: bool) -> List[str]:
    if random_:
        random.shuffle(rooms)
        return rooms
    length_rooms = len(rooms)
    iteration = length_rooms if length_rooms < 5 else 5
    rooms = rooms[:iteration]
    return rooms


def rooms_formatted(rooms: list) -> str:
    if rooms == []:
        return
    start = '- '
    style = '<code>{}</code>'
    rooms_formatted = [start + style.format(room) for room in rooms]
    rooms_over_text = '\n'.join(rooms_formatted)
    return rooms_over_text


def validate_kick_user_index(kick_user_id: str, max_users_id: int) -> Tuple[Union[bool, str]]:
    if not kick_user_id.isdecimal():
        return (False, 'no_number')
    if kick_user_id == '0':
        return (False, 'kick_admin')
    if int(kick_user_id) > max_users_id:
        return (False, 'long_id')
    return (True, ...)


def validate_get_user_index(user_index: str) -> bool:
    if not user_index.isdecimal():
        return False
    if not (-1 < int(user_index) < 11):
        return False
    return True


def index_formatted(length: int) -> str:
    style = '<b>{}</b>'
    indexes = [style.format(number) for number in range(length)]
    indexes_over_text = ', '.join(indexes)
    return indexes_over_text


def get_name(profile: dict = None) -> str:
    if profile:
        nickname = profile.get('nickname', config.standart.standart_name)
    else:
        nickname = config.standart.standart_name
    return nickname


def get_description(profile: dict) -> str:
    description = profile.get('description', config.standart.standart_description)
    return description


def get_photo(profile: dict) -> Union[str, None]:
    photo = profile.get('photo')
    return photo


async def time_sleep(type_sleep: str):
    await asyncio.sleep(TIME_SLEEP_BY_TYPE[type_sleep])
