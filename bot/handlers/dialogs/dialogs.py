from aiogram_dialog import Dialog

from bot.handlers.dialogs.windows import (
    main_window,
    chats_joined_window,
    captcha_message_window,
)


statistics_dialog = Dialog(
    main_window,
    chats_joined_window,
    captcha_message_window
)
