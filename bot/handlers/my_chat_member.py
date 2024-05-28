from aiogram import types, Router
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION
)
from bot.utils.repositories import increment_joined_chats_counter


router = Router()


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def on_chat_join(event: types.ChatMemberUpdated):
    """Увеличить счётчик добавления в чаты на 1."""
    await increment_joined_chats_counter()
