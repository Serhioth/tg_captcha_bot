from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from bot.handlers.dialogs.states import StatisticsMenuState
from bot.filters.is_superadmin import IsSuperadminFilter


router = Router()
router.message.filter(IsSuperadminFilter())


@router.message(Command(commands=["start"]))
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=StatisticsMenuState.main_window,
        mode=StartMode.RESET_STACK
    )
