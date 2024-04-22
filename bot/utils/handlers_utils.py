from aiogram import Bot, html, types
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from motor.core import AgnosticCollection

from bot.core.configure_logging import logger
from bot.core.db_config import DatabaseManager


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


async def get_banned_users_collection():
    """
    Функция для соединения с бд и получения коллекции забаненных пользователей.
    """

    db_manager = DatabaseManager()
    db = await db_manager.get_db()
    collection = db.banned_users

    return collection


async def save_banned_user(user_id: int,
                           user_full_name: str,
                           collection: AgnosticCollection) -> None:
    """
    Функция для добавления пользователя в коллекцию banned_users.
    Необходима для последующего разбана.
    """

    banned_user_data = {
        '_id': user_id,
        'full_name': user_full_name,
    }

    saved_data = await collection.insert_one(banned_user_data)

    logger.info(f'Пользователь {user_id} заблокирован.')
    logger.info(f'Данные сохранены: {repr(saved_data.inserted_id)}')


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
