from aiogram import Bot, html, types
from aiogram.fsm.context import FSMContext

from bot.core.config import settings
from bot.utils.redis import (
    get_user_attempts_number,
    increment_user_attempts_number,
    set_user_attempts_number,
    remove_user_attempts_record
)


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


async def reset_user_attempts_number(user_id: str):
    """Функция для сброса счётчика попыток входа пользователя."""
    user_attempts = await get_user_attempts_number(user_id)

    if user_attempts:
        await remove_user_attempts_record(user_id)


async def check_user_attempts_is_over(user_id: str,) -> bool:
    """
    Функция для проверки счётчика попыток входа пользователя.
    Возвращает True если попытки кончились.
    """
    user_join_attempts = await get_user_attempts_number(user_id)

    if user_join_attempts:
        user_join_attempts = int(user_join_attempts)

        if user_join_attempts > settings.max_captcha_attempts:
            return True
        else:
            await increment_user_attempts_number(user_id)
            return False
    else:
        await set_user_attempts_number(user_id)
        return False
