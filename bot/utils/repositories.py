from bot.core.config import settings
from bot.repositories import (
    DailyMessagesFailedRepository,
    DailyMessagesPassedRepository,
    UserAttemptsRepository,
    JoinedChatsRepository
)


async def reset_user_attempts_number(user_id: str):
    """Функция для сброса счётчика попыток входа пользователя."""
    user_attempts_manager = UserAttemptsRepository(user_id=int(user_id))
    attempts_number = await user_attempts_manager.get()

    if attempts_number:
        await user_attempts_manager.delete()


async def process_user_attempts(user_id: str,) -> bool:
    """
    Функция для проверки счётчика попыток входа пользователя.
    Возвращает True если попытки кончились.
    """
    user_attempts_repository = UserAttemptsRepository(user_id=int(user_id))
    user_join_attempts = await user_attempts_repository.get()

    if isinstance(user_join_attempts, int):
        if user_join_attempts > settings.max_captcha_attempts:
            return True
        else:
            await user_attempts_repository.increment()
            return False


async def get_joined_chats_counter() -> int:
    """Получить количество чатов, куда был добавлен бот."""
    joined_chats_repository = JoinedChatsRepository()
    return await joined_chats_repository.get()


async def increment_joined_chats_counter() -> None:
    """Увеличить счётчик чатов, куда был добавлен бот, на 1."""
    joined_chats_repository = JoinedChatsRepository()
    await joined_chats_repository.increment()


async def get_daily_passed_captcha_messages() -> int:
    """Получить счётчик пройденных каптч за последие 24 часа."""
    daily_passed_messages_repository = DailyMessagesPassedRepository()
    return await daily_passed_messages_repository.get()


async def increment_daily_passed_captcha_messages() -> int:
    """Увеличить счётчик пройденных каптч на 1."""
    daily_passed_messages_repository = DailyMessagesPassedRepository()
    await daily_passed_messages_repository.increment()


async def get_daily_failed_captcha_messages() -> int:
    """Получить счётчик не пройденных каптч за последние 24 часа."""
    daily_failed_messages_repository = DailyMessagesFailedRepository()
    return await daily_failed_messages_repository.get()


async def increment_daily_failed_captcha_messages() -> None:
    """Увеличить счётчик не пройденных каптч на 1."""
    daily_failed_messages_repository = DailyMessagesFailedRepository()
    await daily_failed_messages_repository.increment()
