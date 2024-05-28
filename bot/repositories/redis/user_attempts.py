from .redis import RedisRepository


class UserAttemptsRepository(RedisRepository):
    """Репозиторий для хранения количества попыток входа пользователя."""

    async def __init__(self, user_id: int):
        key = f"user_attempts_{user_id}"
        await super().__init__(key=key)
