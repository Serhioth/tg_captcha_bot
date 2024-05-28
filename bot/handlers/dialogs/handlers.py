from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.dialogs.states import StatisticsMenuState


async def on_joined_chats_button(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager
):
    """Перейти к окну со статистикой чатов."""
    await manager.switch_to(StatisticsMenuState.joined_chats_window)


async def on_captcha_messages_button(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager
):
    """Перейти к окну со статистикой отправленных сообщений."""
    await manager.switch_to(StatisticsMenuState.captcha_messages_window)
