from aiogram import Dispatcher


def setup_filters(dispatcher: Dispatcher):
    from .is_media_group import IsMediaGroup

    dispatcher.filters_factory.bind(IsMediaGroup)
