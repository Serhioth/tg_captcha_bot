from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format

from bot.handlers.dialogs.getters import (
    captcha_message_window_get_data,
    joined_chats_window_get_data,
    main_window_get_data
)
from bot.handlers.dialogs.handlers import (
    on_captcha_messages_button,
    on_joined_chats_button,
)
from bot.handlers.dialogs.states import StatisticsMenuState


main_window = Window(
    Format(
        'Приветствую, {name}!\n'
        'Доступна следующая статистика:'
    ),
    Button(
        Const('Статистика по добавлениям в чаты'),
        id='chats_joined',
        on_click=on_joined_chats_button
    ),
    Button(
        Const('статистика по сообщениям'),
        id='captcha_messages',
        on_click=on_captcha_messages_button
    ),
    state=StatisticsMenuState.main_window,
    getter=main_window_get_data
)

chats_joined_window = Window(
    Format(
        'Количество чатов, в которые добавлен бот: {chats_count}'
    ),
    Back(Const('Назад')),
    state=StatisticsMenuState.joined_chats_window,
    getter=joined_chats_window_get_data
)

captcha_message_window = Window(
    Format(
        'Количество пройденных каптч'
        ' за последние 24 часа: {passed_captcha_messages}\n'
        'Количество не пройденных каптч'
        ' за последние 24 часа: {failed_captcha_messages}\n'
        'Общее количество отправленных за 24'
        ' часа каптч: {total_captcha_messages}'
    ),
    Back(Const('Назад')),
    state=StatisticsMenuState.captcha_messages_window,
    getter=captcha_message_window_get_data
)
