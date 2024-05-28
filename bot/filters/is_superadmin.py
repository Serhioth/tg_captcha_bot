from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.config import settings


class IsSuperadminFilter(BaseFilter):
    """Проверить, что пользователь - суперадминистратор."""
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.bot_superadmins
