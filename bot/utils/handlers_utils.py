from aiogram import Bot, html, types
from aiogram.fsm.context import FSMContext
from redis.asyncio import Redis

from bot.core.config import settings


def protect_username(full_name: str):
    """Защита имени пользователя от XSS."""

    return html.quote(full_name)


async def answer_cancelled(
    message: types.Message,
    state: FSMContext,
    text: str
):
    """Функция для очистки стейта и удаления сообщения,
    если пользователь не ответил за отведённое время."""

    await state.clear()
    await message.delete()
    await message.answer(
        text=text
    )


async def ban_user(
    bot: Bot,
    chat_id: int,
    user_id: int,
    kick: bool = False,
    state: FSMContext = None,
):
    """
    Функция для забанивания пользователя.
    Если передан параметр kick=True, то польбзователь
    будет разбанен с возможностью снова попробовать вступить в группу.
    """

    if kick:
        await bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        await bot.unban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
    else:
        await bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        if state:
            await state.clear()

        return None


async def check_user_attempts(
    event: types.ChatMemberUpdated,
    redis: Redis
) -> bool:
    """
    Функция для проверки счётчика попыток входа пользователя.
    Возвращает True если попытки кончились и пользователь забанен.
    """

    user_join_attempts = await redis.get(event.from_user.id)

    if user_join_attempts:
        user_join_attempts = int(user_join_attempts)
        if user_join_attempts > settings.max_captcha_attempts:
            await ban_user(
                bot=event.bot,
                chat_id=event.chat.id,
                user_id=event.from_user.id,
            )
            return True
        else:
            await redis.incr(event.from_user.id)
            return False
    else:
        await redis.set(event.from_user.id, 1)
        return False
