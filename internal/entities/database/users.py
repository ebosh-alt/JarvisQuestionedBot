import asyncio
from datetime import datetime, timezone

from sqlalchemy import Column, String, BigInteger, DateTime

from pkg.google_client import GoggleClient
from . import *
from .base import Base, BaseDB


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    city = Column(String)
    closer_choice = Column(String)
    preferred_pattern = Column(String)
    attraction_mode = Column(String)
    metaphor_preference = Column(String)
    ai_level = Column(String)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "city": self.city,
            "closer_choice": self.closer_choice,
            "preferred_pattern": self.preferred_pattern,
            "attraction_mode": self.attraction_mode,
            "metaphor_preference": self.metaphor_preference,
            "created_at": self.created_at,
        }


class Users(BaseDB[User]):
    def __init__(self):
        super().__init__(User)

    async def new(self, obj: User):
        await self._add_obj(obj)
        asyncio.create_task(GoggleClient.append(obj, "users"))

    async def get(self, id: int) -> User | None:
        return await self._get_object(id)

    async def update(self, obj: User) -> None:
        await self._update_obj(instance=obj)
        asyncio.create_task(GoggleClient.update(obj, "users"))

    async def delete(self, obj: User) -> None:
        await self._delete_obj(instance=obj)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if isinstance(result, User):
            return result
        return False

    async def get_all(self) -> list[User]:
        return await self._get_objects()

    async def get_all_dict(self) -> list[dict]:
        data = await self.get_all()
        return [user.dict() for user in data]

    async def count(self) -> int:
        objs = await self.get_all()
        return len(objs)
