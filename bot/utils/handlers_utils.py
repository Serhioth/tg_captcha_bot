from aiogram import Bot, html, types
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext

from bot.core.configure_logging import logger


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


async def check_user_id(
    callback: types.CallbackQuery,
    state: FSMContext,
    alert_message: str
) -> None:
    """
    Функция для проверки идентификатора ответившего пользователя.
    """

    state_data = await state.get_data()
    try:
        target_user_id = state_data['target_user_id']
    except KeyError:
        logger.error('Не найден идентификатор целевого пользователя.')
        await state.clear()

        return None

    if callback.from_user.id != target_user_id:
        await callback.answer(
            text=alert_message,
            show_alert=True
        )
        await state.clear()
        return None


async def ban_user(
    bot: Bot,
    chat_id: int,
    user_id: int,
    state: FSMContext = None
):
    """Функция для забанивания пользователя."""

    try:
        await bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

    except TelegramAPIError as error:
        logger.exception(
            'Ошибка при бане пользователя.\n'
            f'Ошибка: {error}'
        )

    if state:
        await state.clear()

    return None
