from aiogram.filters import Filter
from aiogram.types import Message, User

from config import Config

config = Config.load()

class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        if event_from_user.id in config.telegram.admins:
            return True
        return False
