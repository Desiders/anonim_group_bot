from aiogram.types import Message
from app.services.database import RedisDB

from ..scripts.functions import get_text


async def command_info(call: Message, database: RedisDB) -> None:
    arg = call.get_args()
    server, rooms_count, users_count = await database.get_info()
    if arg == '+':
        memory = '\n'.join(f'{item[0]}:{item[1]}' for item in server.get('memory').items())
        stats = '\n'.join(f'{item[0]}:{item[1]}' for item in server.get('stats').items())
        keyspace = '\n'.join(f'{item[0]}:{item[1]}' for item in server.get('keyspace').items())

        await call.answer(get_text('info_super').format(memory, stats,
                                                        keyspace, rooms_count,
                                                        users_count))
    else:
        error_data = 'данные отсутствуют'
        memory_use = server['memory'].get('used_memory_human', error_data)
        memory_use_peak = server['memory'].get('used_memory_peak_human', error_data)
        instantaneous_sec = server['stats'].get('instantaneous_ops_per_sec', error_data)
        keyspace = server['keyspace'].setdefault('db0', {}).get('keys', 0)

        await call.answer(get_text('info').format(memory_use, memory_use_peak,
                                                  instantaneous_sec, keyspace,
                                                  rooms_count, users_count))