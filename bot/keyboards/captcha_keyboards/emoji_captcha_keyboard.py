import random

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import UserJoinCallback
from utils.hash import generate_hash


buttons_choices = ['🦑', '🐙', '🦕', '🦖', '🦎', '🐍',
                   '🪰', '🪲', '🪳', '🦟', '🦗', '🕷',
                   '🦋', '🐛', '🪱', '🐝', '🫎', '🦄',
                   '🪿', '🦆', '🐦‍⬛️', '🦅', '🦉', '🦇',
                   '🐳', '🐬', '🐟', '🐠', '🐡', '🦀']


def generate_captcha_keyboard() -> tuple[InlineKeyboardBuilder, dict]:
    """
    Конструктор клавиатуры с вариантами ответа.
    Возвращает верную кнопку и сгенерированную клавиатуру.
    """
    keyboard = InlineKeyboardBuilder()
    choiced_buttons = random.sample(buttons_choices, 4)
    buttons = []

    for button in choiced_buttons:
        buttons.append({
            'text': button,
            'callback_data': UserJoinCallback(
                description='captcha_answer',
                value=generate_hash()
            )
        })

    true_button = random.choice(buttons)

    for button in buttons:
        keyboard.button(**button)

    keyboard.adjust(2, repeat=True)
    return keyboard, true_button
