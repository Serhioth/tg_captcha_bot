from aiogram_dialog import DialogManager

from bot.utils.repositories import (
    get_daily_failed_captcha_messages,
    get_daily_passed_captcha_messages,
    get_joined_chats_counter,
)
from bot.utils.handlers import protect_username


async def main_window_get_data(
    dialog_manager: DialogManager,
    **kwargs,
):
    """Получить имя пользователя через DialogManager."""
    user = dialog_manager.event.from_user
    user_first_name = protect_username(user.first_name)
    return {'name': user_first_name}


async def joined_chats_window_get_data(**kwargs):
    """Получить количество чатов, в которые был добавлен бот."""
    return {'chats_count': await get_joined_chats_counter()}


async def captcha_message_window_get_data(**kwargs):
    """Получить статистику о прохождении каптч."""
    return {
        'passed_captcha_messages': await get_daily_passed_captcha_messages(),
        'failed_captcha_messages': await get_daily_failed_captcha_messages(),
        'total_captcha_messages': (
            await get_daily_passed_captcha_messages()
            + await get_daily_failed_captcha_messages()
        ),
    }
