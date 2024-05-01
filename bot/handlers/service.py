# from aiogram import F, Router
# from aiogram.filters.chat_member_updated import (
#     ChatMemberUpdatedFilter,
#     IS_NOT_MEMBER,
#     MEMBER,
#     ADMINISTRATOR,
#     KICKED,
#     LEFT,
#     RESTRICTED,
#     CREATOR
# )
# from aiogram.types import ChatMemberUpdated
# from aioredis.client import Redis
# from fastapi import Depends

# from bot.core.db import get_redis

# router = Router()

# router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


# @router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=IS_NOT_MEMBER | MEMBER >> ADMINISTRATOR
#     )
# )
# async def on_chat_join(
#     event: ChatMemberUpdated,
#     redis: Redis = Depends(get_redis)
# ):
#     """
#     Функция для сохранения начальных настроек чата
#     при добавлении бота в чат.
#     """

#     admins = event.chat.get_administrators()
#     admins_ids = [admin.id for admin in admins]

#     await redis.set(
#         name=f'{event.chat.id}',
#         value=admins_ids,
#     )
