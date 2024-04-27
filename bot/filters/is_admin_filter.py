from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsGroupAdminFilter(BaseFilter):
    """
    Фильтр для проверки того, что пользователь
    является администратором группы.
    """

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in message.chat.get_administrators()
