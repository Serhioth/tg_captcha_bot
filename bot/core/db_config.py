from motor import motor_asyncio
from bot.core.constants import MONGODB_URL


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._db = None
        return cls._instance

    async def get_db(self):
        if self._db is None:
            client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
            self._db = client['azcaban']
        return self._db
