import random

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import UserJoinCallback


buttons_choices = ['🦑', '🐙', '🦕', '🦖', '🦎', '🐍',
                   '🪰', '🪲', '🪳', '🦟', '🦗', '🕷',
                   '🦋', '🐛', '🪱', '🐝', '🫎', '🦄',
                   '🪿', '🦆', '🐦‍⬛️', '🦅', '🦉', '🦇',
                   '🐳', '🐬', '🐟', '🐠', '🐡', '🦀']


def generate_captcha_keyboard() -> tuple[InlineKeyboardBuilder, str]:
    """
    Конструктор клавиатуры с вариантами ответа.
    Возвращает верную кнопку и сгенерированную клавиатуру.
    """

    keyboard = InlineKeyboardBuilder()
    buttons = random.sample(buttons_choices, 4)
    true_button = random.choice(buttons)

    for button in buttons:
        keyboard.button(
            text=button,
            callback_data=UserJoinCallback(
                description='captcha_answer',
                value='correct' if button == true_button else 'incorrect'
            )
        )

    keyboard.adjust(2, repeat=True)
    return keyboard, true_button
