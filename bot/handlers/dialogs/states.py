from aiogram.fsm.state import StatesGroup, State


class StatisticsMenuState(StatesGroup):
    """Класс для работы с меню просмотра статистики."""
    main_window = State()
    joined_chats_window = State()
    captcha_messages_window = State()
