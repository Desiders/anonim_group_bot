from . import config, handlers


def load_config(path: str) -> config.Config:
    return config.load_config(path)


def register_handlers(dispatcher: handlers.Dispatcher) -> None:
    handlers.register_handlers(dispatcher)
