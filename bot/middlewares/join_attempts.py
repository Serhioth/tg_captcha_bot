from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware, types

from bot.core.config import bot, settings
from bot.utils.handlers_utils import ban_user


class JoinAttemptsMiddleware(BaseMiddleware):
    """
    Миддлварь для проверки количества попыток войти в чат у пошльзователя.
    Если количество попыток выше заданного администраторм - пользователь
    банится насовсем.
    """

    def __init__(self):
        super().__init__()
        self.join_attempts = {}

    async def __call__(
            self,
            handler: Callable[
                [types.TelegramObject, Dict[str, Any]],
                Awaitable[Any]
            ],
            event: types.TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, types.Message) and event.new_chat_members:
            await self.on_pre_process_message(event, data)
        return await handler(event, data)

    async def on_pre_process_message(
        self,
        event: types.TelegramObject,
        data: dict
    ):
        for member in event.new_chat_members:
            if member.id not in self.join_attempts:
                self.join_attempts[str(member.id)] = 0
                self.join_attempts[str(member.id)] += 1

            if (
                self.join_attempts[str(member.id)]
                > settings.max_captcha_attempts
            ):
                await ban_user(
                    bot=bot,
                    chat_id=event.chat.id,
                    user_id=member.id
                )
