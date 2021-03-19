from aiogram import Dispatcher

from .is_media_group import IsMediaGroup


def setup_filters(dispatcher: Dispatcher):
    dispatcher.filters_factory.bind(IsMediaGroup)