from aiogram import enums, F, types, Router

from bot.core.config import bot

router = Router()


@router.message(
    F.from_user.id == bot.id,
    F.content_type == enums.ContentType.LEFT_CHAT_MEMBER,
)
async def remove_own_user_leave_message(message: types.Message):
    """
    Функция для удаления сервисного сообщения о том,
    что бот исключил пользователя из чата.
    """

    await message.delete()
