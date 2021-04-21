from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, database):
        super().__init__()
        self.database = database

    async def pre_process(self, obj, data, *args):
        data["database"] = self.database
