from .redis import RedisRepository


class JoinedChatsRepository(RedisRepository):
    """
    Репозиторий для хранения количества чатов, куда был добавлен бот.
    """
    async def __init__(self):
        key = "joined_chats"
        await super().__init__(key=key)
