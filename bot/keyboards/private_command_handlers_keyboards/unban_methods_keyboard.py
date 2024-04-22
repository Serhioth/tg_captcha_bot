from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import UnbanOptionCallback


def generate_unban_options_keyboard():
    """Генерирует клавиатуру для выбора метода разбанивания пользователя."""

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text='Разбанить по айди',
        callback_data=UnbanOptionCallback(
            description='unban_option',
            value='id_unban'
        )
    )
    keyboard.button(
        text='Разбанить по полному имени',
        callback_data=UnbanOptionCallback(
            description='unban_option',
            value='full_name_unban'
        )
    )
    keyboard.button(
        text='Выбрать из списка',
        callback_data=UnbanOptionCallback(
            description='unban_option',
            value='list_unban'
        )
    )

    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
