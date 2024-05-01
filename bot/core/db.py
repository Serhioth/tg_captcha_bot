from redis.asyncio import Redis

from .config import redis_url


async def get_redis():
    """Функция для подключения к Redis."""
    redis = await Redis.from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True
    )
    return redis
