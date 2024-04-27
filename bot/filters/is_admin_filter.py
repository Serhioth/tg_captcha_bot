from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsGroupAdminFilter(BaseFilter):
    """
    Фильтр для проверки того, что пользователь
    является администратором группы.
    """

    async def __call__(self, message: Message) -> bool:
        admins = await message.chat.get_administrators()
        admins_id = [admin.user.id for admin in admins]
        return message.from_user.id in admins_id
