from configparser import ConfigParser
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
    max_length_nickname: int
    max_length_description: int
    standart_name: str
    standart_description: str
    time_sleep_new_member: float
    time_sleep_kick_member: float
    time_sleep_leave_member: float
    time_sleep_new_message_single: float
    time_sleep_new_message_group: float


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    standart: StandartValueConfig


def load_config(path: str) -> Config:
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
                      max_length_nickname=int(standart['max_length_nickname']),
                      max_length_description=int(standart['max_length_description']),
                      standart_name=standart['standart_name'],
                      standart_description=standart['standart_description'],
                      time_sleep_new_member=float(standart['time_sleep_new_member']),
                      time_sleep_kick_member=float(standart['time_sleep_kick_member']),
                      time_sleep_leave_member=float(standart['time_sleep_leave_member']),
                      time_sleep_new_message_single=float(standart['time_sleep_new_message_single']),
                      time_sleep_new_message_group=float(standart['time_sleep_new_message_group'])))
