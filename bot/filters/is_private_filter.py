from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivateFilter(BaseFilter):
    """
    Фильтр для проверки того, что тип чата - приватный.
    """
    async def __call__(self, obj: Message):
        return obj.chat.type == 'private'
