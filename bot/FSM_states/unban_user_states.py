from aiogram.fsm.state import StatesGroup, State


class UnbanUserStates(StatesGroup):
    """FSM-стейты для разблокировки забаненных пользователей."""

    start_process = State()
    select_option = State()
    id_unban = State()
    full_name_unban = State()
    list_unban = State()
    confirm_list_unban = State()
    unban_confirmed = State()
