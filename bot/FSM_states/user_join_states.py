from aiogram.fsm.state import StatesGroup, State


class UserJoinStates(StatesGroup):
    """FSM стейты для обработки вступления в группу."""

    waiting_for_answer = State()
    process_answer = State()
    process_correct_answer = State()
    process_incorrect_answer = State()
    process_timeout = State()
