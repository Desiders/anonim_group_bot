from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str
    db: int


@dataclass
class StandartValueConfig:
    min_length_nickname: int
    max_length_nickname: int
    min_length_description: int
    max_length_description: int
    standart_name: str
    standart_description: str
    time_sleep_new_member: float
    time_sleep_end_member: float
    time_sleep_new_message_single: float
    time_sleep_new_message_group: float


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    standart: StandartValueConfig


def load_config(path: str) -> Config:
    from configparser import ConfigParser

    config = ConfigParser()
    config.read(path, encoding='utf-8')

    redis_config = config['RedisConfig']
    standart = config['StandartValueConfig']

    return Config(bot=BotConfig(**config['BotConfig']),
                  redis=RedisConfig(
                      host=redis_config['host'],
                      port=int(redis_config['port']),
                      password=redis_config['password'],
                      db=int(redis_config['db'])),
                  standart=StandartValueConfig(
                      min_length_nickname=int(standart['min_length_nickname']),
                      max_length_nickname=int(standart['max_length_nickname']),
                      min_length_description=int(standart['min_length_description']),
                      max_length_description=int(standart['max_length_description']),
                      standart_name=standart['standart_name'],
                      standart_description=standart['standart_description'],
                      time_sleep_new_member=float(standart['time_sleep_new_member']),
                      time_sleep_end_member=float(standart['time_sleep_end_member']),
                      time_sleep_new_message_single=float(standart['time_sleep_new_message_single']),
                      time_sleep_new_message_group=float(standart['time_sleep_new_message_group'])))
