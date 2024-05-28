from typing import Optional, Union

from bot.core.config import redis_client, bot
from bot.repositories.base import AbstractRepository


class RedisRepository(AbstractRepository):
    """Реализация репозитория для Redis."""

    async def __init__(self, key: str, expire: Optional[int] = None) -> None:
        self.bot_id = bot.id
        self.key = f'{self.bot_id}:{key}'
        self.redis_client = redis_client

        if await self.redis_client.get(self.key) is None:
            if expire:
                await self.redis_client.setex(self.key, expire, 0)
            else:
                await self.redis_client.set(self.key, 0)

    async def get(self):
        """Получить значение ключа Redis."""
        value = await self.redis_client.get(self.key)
        if value is not None:
            value = value.decode('utf-8')
            try:
                value = int(value)
            except ValueError:
                pass

        return value

    async def add(self, value: Union[str, int],):
        """Создать новую запись в Redis."""
        return await self.redis_client.set(name=self.key, value=value)

    async def delete(self):
        """Удалить запись в Redis."""
        return await self.redis_client.delete(self.key)

    async def increment(self):
        """Увеличить зачение ключа Redis на 1."""
        return await self.redis_client.incr(self.key)
