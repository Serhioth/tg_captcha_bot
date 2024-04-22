from aiogram import F, types, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext

from bot.callbacks.callback_fabs import (
    ConfirmationCallback,
    UnbanOptionCallback,
    PaginationCallback
)
from bot.core.configure_logging import logger
from bot.core.constants import (
    TELEGRAM_GROUP_ID
)
from bot.core.db_config import DatabaseManager
from bot.FSM_states.unban_user_states import UnbanUserStates
from bot.utils.handlers_utils import (
    answer_cancelled,
    protect_username
)
from bot.keyboards.private_command_handlers_keyboards import (
    generate_banned_users_keyboard,
    generate_confirm_keyboard
)
from bot.translations.ru.private_command_messages import (
    CANCEL_MESSAGE,
    CONFIRM_MESSAGE,
    CHOICE_SELECT_MESSAGE,
    ID_UNBAN_MESSAGE,
    FULL_NAME_UNBAN_MESSAGE,
    FINISH_UNBAN_MESSAGE,
    UNBAN_MESSAGE,
    NO_BANNED_USERS_MESSAGE
)

router = Router()


# Хэндлеры для обработки команд администратора в приватном чате.

@router.callback_query(
    UnbanOptionCallback.filter(
        F.value == 'id_unban'
    )
)
async def process_id_unban_option(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Хэндлер для освобождения из бан-листа по Telegram ID пользователя."""

    await state.set_state(UnbanUserStates.id_unban)

    await callback.message.answer(
        text=ID_UNBAN_MESSAGE
    )


@router.callback_query(
    UnbanOptionCallback.filter(
        F.value == 'full_name_unban'
    )
)
async def process_full_name_unban_option(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Хэндлер для освобождения из бан-листа по полному имени пользователя."""

    await state.set_state(UnbanUserStates.full_name_unban)

    await callback.message.answer(
        text=FULL_NAME_UNBAN_MESSAGE
    )


@router.callback_query(
    PaginationCallback.filter(
        F.description == 'banned_users'
    )
)
async def confirm_choise(
    callback: types.CallbackQuery,
    callback_data: PaginationCallback,
    state: FSMContext
):
    """Хэндлер для подтверждения выбора."""

    await state.set_state(UnbanUserStates.confirm_list_unban)

    await state.update_data(user_id=callback_data.value)

    username = protect_username(callback.from_user.full_name)

    await callback.message.edit_text(
        text=CHOICE_SELECT_MESSAGE.format(
            username=username,
        ),
        reply_markup=generate_confirm_keyboard()
    )


@router.callback_query(
    UnbanOptionCallback.filter(
        F.value == 'list_unban'
    )
)
async def choose_user_to_unban(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Хэндлер для выбора пользователя для разбанивания."""

    await state.set_state(UnbanUserStates.list_unban)

    user_full_name = protect_username(callback.from_user.full_name)
    keyboard = await generate_banned_users_keyboard()

    if keyboard is None:
        await callback.message.edit_text(
            text=NO_BANNED_USERS_MESSAGE.format(
                username=user_full_name
            )
        )
        await state.clear()
        return

    await callback.message.edit_text(
        text=UNBAN_MESSAGE.format(
            username=user_full_name
        ),
        reply_markup=keyboard
    )


@router.callback_query(
    PaginationCallback.filter(
        F.description == 'page'
    )
)
async def banned_users_pagination_handler(
    callback: types.CallbackQuery,
    callback_data: PaginationCallback,
    state: FSMContext
):
    """Хэндлер для пагинации списка забаненных пользователей."""

    await callback.message.edit_reply_markup(
        reply_markup=await generate_banned_users_keyboard(
            page=int(callback_data.value)
        )
    )


@router.callback_query(
    ConfirmationCallback.filter(
        F.value == 'cancel'
    )
)
async def cancel_command(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Хэндлер для отмены команды."""

    await answer_cancelled(callback.message, state, CANCEL_MESSAGE)


@router.callback_query(
    ConfirmationCallback.filter(
        F.value == 'confirm'
    )
)
async def unban_confirmed(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Хэндлер для обработки подтверждённого разбанивания."""

    await state.set_state(UnbanUserStates.unban_confirmed)

    username = protect_username(callback.from_user.full_name)

    await callback.message.edit_text(
        text=CONFIRM_MESSAGE.format(
            username=username
        )
    )

    data = await state.get_data()
    user_id = data.get('user_id')
    chat_id = TELEGRAM_GROUP_ID

    try:
        await callback.bot.unban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        db_manager = DatabaseManager()
        db = await db_manager.get_db()

        logger.info(f'Пользователь {user_id} разбанен.')

        result = await db.banned_users.delete_one({'_id': int(user_id)})
        logger.info(f'Результат удаления записи: {result.deleted_count}')

        await callback.message.edit_text(
            text=FINISH_UNBAN_MESSAGE.format(
                username=username
            )
        )
        await state.clear()

    except TelegramAPIError as error:
        logger.info(
            'Ошибка при попытке разбанить пользователя.\n'
            f'Ошибка: {error}'
        )
