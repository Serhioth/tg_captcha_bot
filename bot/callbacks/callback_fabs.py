from typing import Optional

from aiogram.filters.callback_data import CallbackData


class CaptchaCallback(CallbackData, prefix='user_join'):
    """Коллбэк-фабрика для хэндлеров user_join."""

    description: str
    value: Optional[str]
