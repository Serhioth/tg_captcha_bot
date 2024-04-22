from aiogram import types
from aiogram.filters import BaseFilter

from bot.core.constants import TELEGRAM_GROUP_ID


class IsAllowedGroupMessageFilter(BaseFilter):
    """
    Фильтр для проверки того, что сообщение пришло из разрешённой группы.
    """

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id == TELEGRAM_GROUP_ID


class IsAllowedGroupEventFilter(BaseFilter):
    """
    Фильтр для проверки того, что событие пришло из разрешённой группы.
    """

    async def __call__(self, event: types.ChatMemberUpdated) -> bool:
        return event.chat.id == TELEGRAM_GROUP_ID
