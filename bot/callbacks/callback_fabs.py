from typing import Optional, Union

from aiogram.filters.callback_data import CallbackData


class ConfirmationCallback(CallbackData, prefix='choice'):
    """Коллбэк-фабрика для клавиатуры с подтверждением выбора."""

    description: str
    value: Optional[Union[str, int]]


class UserJoinCallback(CallbackData, prefix='user_join'):
    """Коллбэк-фабрика для хэндлеров user_join."""

    description: str
    value: Optional[str]


class PaginationCallback(CallbackData, prefix='keyboard_pagination'):
    """Коллбэк-фабрика для клавиатуры с забаненными пользователями."""

    description: str
    value: Optional[Union[str, int]]


class UnbanOptionCallback(CallbackData, prefix='unban_option'):
    """Коллбэк-фабрика для клавиатуры с выбором опции разбана."""

    description: str
    value: Optional[Union[str, int]]
