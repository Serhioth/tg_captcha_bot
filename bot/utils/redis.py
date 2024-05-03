from bot.core.config import redis_client


async def get_user_attempts_number(user_id: str) -> int:
    """Получить количество попыток входа пользователя из Redis."""
    return await redis_client.get(user_id)


async def increment_user_attempts_number(key: str) -> None:
    """Увеличить ключ Redis на 1."""
    return await redis_client.incr(key)


async def set_user_attempts_number(user_id: str, attempts_number: int = 0):
    """
    Установить количество попыток пользователя,
    по умолчанию устанавливает количество 0.
    """
    return await redis_client.set(user_id, attempts_number)


async def remove_user_attempts_record(user_id: str):
    """Удалить запись о попытках входа пользователя."""
    return await redis_client.delete(user_id)
