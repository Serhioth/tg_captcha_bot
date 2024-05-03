from aiogram.fsm.state import StatesGroup, State


class UserJoinStates(StatesGroup):
    """FSM стейты для обработки вступления в группу."""

    waiting_for_answer = State()
    process_answer = State()
    process_timeout = State()
    attempts_limit_reached = State()
