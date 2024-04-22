from aiogram import types, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.filters.is_admin_filter import IsGroupAdminFilter
from bot.filters.is_private_filter import IsPrivateFilter
from bot.FSM_states.unban_user_states import UnbanUserStates
from bot.utils.handlers_utils import protect_username
from bot.keyboards.private_command_handlers_keyboards import (
    generate_unban_options_keyboard
)
from bot.translations.ru.private_command_messages import (
    HELP_MESSAGE,
    START_MESSAGE,
)


router = Router()
router.message.filter(IsGroupAdminFilter(), IsPrivateFilter())


@router.message(CommandStart())
async def start_command(message: types.Message,):
    """Хэндлер для обработки комманды /start."""

    username = protect_username(message.from_user.full_name)

    await message.answer(
        START_MESSAGE.format(
            username=username
        )
    )


@router.message(Command('help'))
async def help_command(message: types.Message):
    """Хэндлер для обработки команды /help."""

    await message.answer(
        text=HELP_MESSAGE
    )


@router.message(Command('unban'))
async def unban_command(message: types.Message, state: FSMContext):
    """Команда для разбанивания пользователей."""

    await state.set_state(UnbanUserStates.start_process)

    username = protect_username(message.from_user.full_name)
    unban_options_keyboard = generate_unban_options_keyboard()

    await message.answer(
        text=f'Выбери способ, {username}',
        reply_markup=unban_options_keyboard
    )
