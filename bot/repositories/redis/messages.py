from .redis import RedisRepository


class DailyMessagesFailedRepository(RedisRepository):
    """
    Репзоиторий для хранения количества не успешно пройденных каптч.
    Хранит информацию за последние 24 часа.
    """

    async def __init__(self) -> None:
        key = 'daily_messages_failed'
        expire = 86400  # 24 часа
        await super().__init__(key=key, expire=expire)


class DailyMessagesPassedRepository(RedisRepository):
    """
    Репозиторий для хранения количества успешно пройденных каптч.
    Хранит информацию за последние 24 часа.
    """

    async def __init__(self) -> None:
        key = 'daily_messages_passed'
        expire = 86400  # 24 часа
        await super().__init__(key=key, expire=expire)
