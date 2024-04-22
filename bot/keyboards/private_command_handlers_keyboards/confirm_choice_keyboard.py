from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import ConfirmationCallback


def generate_confirm_keyboard() -> InlineKeyboardBuilder:
    """Генерирует клавиатуру для подтверждения действия"""

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text='Да',
        callback_data=ConfirmationCallback(
            description='choice',
            value='confirm'
        )
    )
    keyboard.button(
        text='Нет',
        callback_data=ConfirmationCallback(
            description='choice',
            value='cancel'
        )
    )

    keyboard.adjust(2)
    return keyboard.as_markup()
