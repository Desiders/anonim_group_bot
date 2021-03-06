import asyncio
from typing import Dict, List, Optional, Tuple, Union

import aioredis

from ..scripts.functions import (generate_key, generate_key_users,
                                 generate_room_id)

ROOM_KEY = 'room'
USER_KEY = 'user'
PROFILE_KEY = 'profile'
ROOMS_KEY = 'rooms'
MAX_LENGTH_ROOM = 10


class RedisDB:
    def __init__(self, host: str, port: int, password: str, db: int) -> None:
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self._loop = asyncio.get_event_loop()

        self._redis: Optional[aioredis.RedisConnection] = None
        self._connection_lock = asyncio.Lock(loop=self._loop)
    
    async def close(self) -> None:
        async with self._connection_lock:
            if self._redis and not self._redis.closed:
                self._redis.close()

    async def wait_closed(self) -> None:
        async with self._connection_lock:
            if self._redis:
                await self._redis.wait_closed()
    
    async def redis(self) -> aioredis.Redis:
        async with self._connection_lock:
            if self._redis is None or self._redis.closed:
                self._redis = await aioredis.create_redis_pool((self._host, self._port),
                                                                password=self._password,
                                                                db=self._db,
                                                                encoding='utf-8',)
        return self._redis

    # Активные комнаты
    async def get_rooms(self) -> List[str]:
        redis = await self.redis()
        rooms = await redis.hgetall(ROOMS_KEY)
        return rooms

    # Получить информацию о текущей комнате
    async def get_room(self, user_id: int) -> Tuple[bool, Union[Tuple[int, str]]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return (False, ...)

        key_room = generate_key(ROOM_KEY, room_id)
        length = await redis.llen(key_room)
        return (True, (room_id, length))

    # Создать новую комнату
    async def new_room(self, user_id: int) -> Tuple[Union[bool, str]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if room_id:
            return (False, ...)

        room_id = generate_room_id()
        key_room = generate_key(ROOM_KEY, room_id)
        transaction = redis.multi_exec()
        transaction.set(key_user, room_id)
        transaction.hset(ROOMS_KEY, room_id, 1)
        transaction.rpush(key_room, user_id)
        await transaction.execute()
        return (..., room_id)

    # Вступить в комнату по номеру
    async def join_room(self, user_id: int, join_id_room: str) -> Tuple[Union[None, bool],
                                                                        Union[str, Tuple[str, List[int]]]]:
        key_user, join_key_room = generate_key(USER_KEY, user_id), generate_key(ROOM_KEY, join_id_room)
        redis = await self.redis()
        transaction = redis.multi_exec()
        transaction.get(key_user)
        transaction.llen(join_key_room)
        room_id, length = await transaction.execute()
        if not length or length >= MAX_LENGTH_ROOM:
            return (None, join_id_room)

        elif room_id:
            return (False, ...)

        key_user_profile = generate_key(PROFILE_KEY, user_id)
        transaction = redis.multi_exec()
        transaction.set(key_user, join_id_room)
        transaction.hgetall(key_user_profile)
        transaction.lrange(join_key_room, 0, -1)
        transaction.rpush(join_key_room, user_id)
        _, user_profile, users, _ = await transaction.execute()
        return (True, (join_id_room, user_profile, users))
    
    # Выход из комнаты
    async def end_room(self, user_id: int) -> Tuple[Union[None, bool], str]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return (None, ...)

        key_room = generate_key(ROOM_KEY, room_id)
        transaction = redis.multi_exec()
        transaction.unlink(key_user)
        transaction.lrem(key_room, 1, user_id)
        transaction.llen(key_room)
        result = await transaction.execute()
        delete = not result[-1]
        if delete:
            transaction = redis.multi_exec()
            transaction.hset(ROOMS_KEY, room_id, 0)
            transaction.unlink(key_room)
            await transaction.execute()
        return (delete, room_id)

    # Получить временные номера участников комнаты
    async def get_members(self, user_id: int) -> Union[None, List[str]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return None
        
        key_room = generate_key(ROOM_KEY, room_id)
        length = await redis.llen(key_room)
        return length

    # Исключение пользователя из комнаты по его временному номеру
    async def kick_user_over_id_from_room(self, user_id: int, kick_user_index: int) -> Tuple[
                                                                                        Union[bool, None],
                                                                                        Union[bool, str, list]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return (None, ...)

        key_room = generate_key(ROOM_KEY, room_id)
        users = await redis.lrange(key_room, 0, -1)
        max_index_user = len(users) - 1
        if kick_user_index > max_index_user:
            return (False, kick_user_index)

        admin = int(users[0])
        if admin != user_id:
            return (True, False)

        kick_user_id = users[kick_user_index]
        key_kick_user, key_user_profile = generate_key(USER_KEY, kick_user_id), generate_key(PROFILE_KEY, kick_user_id)
        transaction = redis.multi_exec()
        transaction.unlink(key_kick_user)
        transaction.hget(key_user_profile, 'nickname')
        transaction.lrem(key_room, 1, kick_user_id)
        _, kick_user_nickname, _ = await transaction.execute()
        return (True, [kick_user_index, kick_user_nickname, room_id, kick_user_id, users])

    # Изменение номера комнаты на случайный
    async def change_id_room(self, user_id: int) -> Tuple[Union[None, bool], str]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return (None, ...)

        key_room = generate_key(ROOM_KEY, room_id)
        users = await redis.lrange(key_room, 0, -1)
        admin = int(users[0])
        if admin != user_id:
            return (False, ...)

        key_users_room, new_id_room = generate_key_users(USER_KEY, users), generate_room_id(True)
        migrate_users_room = dict.fromkeys(key_users_room, new_id_room)
        new_key_room = generate_key(ROOM_KEY, new_id_room)
        transaction = redis.multi_exec()
        transaction.mset(migrate_users_room)
        transaction.hdel(ROOMS_KEY, room_id)
        transaction.hset(ROOMS_KEY, new_id_room, 1)
        transaction.rename(key_room, new_key_room)
        await transaction.execute()
        return (True, new_id_room)
    
    # Получение своего профиля
    async def get_my_profile(self, user_id: int) -> Dict[str, str]:
        key_user_profile = generate_key(PROFILE_KEY, user_id)
        redis = await self.redis()
        user_profile = await redis.hgetall(key_user_profile)
        return user_profile
    
    # Получение чужого профиля
    async def get_profile(self, user_id: int, user_index: int) -> Union[None, bool, Dict[str, str]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return None

        key_room = generate_key(ROOM_KEY, room_id)
        user_id = await redis.lindex(key_room, user_index)
        if not user_id:
            return False

        key_user_profile = generate_key(PROFILE_KEY, user_id)
        user_profile = await redis.hgetall(key_user_profile)
        return user_profile

    # Редактирование профиля
    async def edit_profile(self, user_id: int, type_object: str, new_object: str) -> None:
        key_user_profile = generate_key(PROFILE_KEY, user_id)
        redis = await self.redis()
        await redis.hset(key_user_profile, type_object, new_object)
    
    # Получить временные номера участников комнаты для отправки сообщения
    async def get_members_over_send(self, user_id: int) -> Union[Tuple[None],
                                                            Tuple[bool],
                                                            Tuple[Dict[str, str], List[str]]]:
        key_user = generate_key(USER_KEY, user_id)
        redis = await self.redis()
        room_id = await redis.get(key_user)
        if not room_id:
            return (..., None)
        
        key_user_profile = generate_key(PROFILE_KEY, user_id)
        key_room = generate_key(ROOM_KEY, room_id)
        transaction = redis.multi_exec()
        transaction.hgetall(key_user_profile)
        transaction.lrange(key_room, 0, -1)
        author, users = await transaction.execute()
        if len(users) == 1:
            return (..., False)
        author['user_index'] = users.index(str(user_id))
        return (author, users)
