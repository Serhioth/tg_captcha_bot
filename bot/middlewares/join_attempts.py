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

    async def __call__(self, message: types.Message, data: dict):
        await self.on_pre_process_message(message, data)

    async def on_pre_process_message(
        self,
        message: types.Message,
        data: dict
    ):
        if message.new_chat_members:
            for member in message.new_chat_members:
                if member.id not in self.join_attempts:
                    self.join_attempts[str(member.id)] = 0
                    self.join_attempts[str(member.id)] += 1

                if (
                    self.join_attempts[str(member.id)]
                    > settings.max_captcha_attempts
                ):
                    await ban_user(
                        bot=bot,
                        chat_id=message.chat.id,
                        user_id=member.id
                    )
