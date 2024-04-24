import time

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.exceptions import TelegramAPIError

from bot.core.constants import (
    RESTRICT_TIMEOUT,
    RESTRICTED_PERMISSIONS
)
from bot.core.configure_logging import logger
from bot.filters import (
    IsAllowedGroupMessageFilter,
    IsGroupAdminFilter
)
from bot.utils.handlers_utils import (
    protect_username
)
from bot.translations.ru.group_commands_messages import (
    BAN_USER_COMMAND_MESSAGE,
    RESTRICT_USER_COMMAND_MESSAGE,
    RESTRICT_WRONG_ARGS_MESSAGE
)


router = Router()
router.message.filter(
    IsAllowedGroupMessageFilter(),
    IsGroupAdminFilter()
)


@router.message(Command('ban'), F.reply_to_message)
async def ban_user(message: types.Message):
    try:

        user_full_name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id

        await message.chat.ban(user_id=user_id)

        await message.reply_to_message.answer(
            BAN_USER_COMMAND_MESSAGE.format(
                username=protect_username(
                    user_full_name
                )
            )
        )
        logger.info
    except TelegramAPIError as error:
        logger.info(f"Ошибка при попытке забанить пользователя: {error}")
        return


@router.message(Command('restrict'), F.reply_to_message)
async def restrict_user(message: types.Message,
                        command: CommandObject):

    user_full_name = protect_username(
        message.reply_to_message.from_user.full_name
    )
    user_id = message.reply_to_message.from_user.id
    admin_full_name = protect_username(message.from_user.full_name)

    utc_now = time.time()

    if command.args is None:
        restrict_time = RESTRICT_TIMEOUT + utc_now
        time_of_restriction = RESTRICT_TIMEOUT
    else:
        try:
            restrict_time = int(command.args) + utc_now
            time_of_restriction = int(command.args)

        except ValueError:
            restrict_time = RESTRICT_TIMEOUT + utc_now
            time_of_restriction = RESTRICT_TIMEOUT

            await message.answer(
                text=RESTRICT_WRONG_ARGS_MESSAGE.format(
                    admin=admin_full_name,
                    username=user_full_name,
                    restrict_time=time_of_restriction,
                )
            )
            logger.info(f'Администратор {admin_full_name} '
                        'ввёл неверные аргументы при попытке '
                        f'ограничить пользователя {user_full_name}')
    try:
        await message.chat.restrict(user_id=user_id,
                                    permissions=RESTRICTED_PERMISSIONS,
                                    until_date=restrict_time,
                                    use_independent_chat_permissions=True)

        await message.reply_to_message.answer(
            text=RESTRICT_USER_COMMAND_MESSAGE.format(
                username=protect_username(
                    user_full_name
                ),
                restrict_time=time_of_restriction
            )
        )
        logger.info(f'Администратор {admin_full_name} '
                    f'ограничил пользователя {user_full_name} '
                    f'на {restrict_time} секунд')

    except TelegramAPIError as error:
        logger.info("Ошибка при попытке наложить"
                    f" ограничения на пользователя: {error}")
