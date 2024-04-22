from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.constants import GROUP_ADMINSTRATOR_IDS


class IsGroupAdminFilter(BaseFilter):
    """
    Фильтр для проверки того, что пользователь
    является администратором группы.
    """

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in GROUP_ADMINSTRATOR_IDS