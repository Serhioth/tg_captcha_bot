import random

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import UserJoinCallback
from utils.hash import generate_hash


buttons_choices = ['🦑', '🐙', '🦕', '🦖', '🦎', '🐍',
                   '🪰', '🪲', '🪳', '🦟', '🦗', '🕷',
                   '🦋', '🐛', '🪱', '🐝', '🫎', '🦄',
                   '🪿', '🦆', '🐦‍⬛️', '🦅', '🦉', '🦇',
                   '🐳', '🐬', '🐟', '🐠', '🐡', '🦀']


def generate_captcha_keyboard(
    chat_id: int,
    user_id: int
) -> tuple[InlineKeyboardBuilder, str]:
    """
    Конструктор клавиатуры с вариантами ответа.
    Возвращает верную кнопку и сгенерированную клавиатуру.
    """
    keyboard = InlineKeyboardBuilder()
    buttons = random.sample(buttons_choices, 4)
    true_button = random.choice(buttons)

    hash_ = generate_hash(chat_id, user_id)

    for button in buttons:
        keyboard.button(
            text=button,
            callback_data=UserJoinCallback(
                description='captcha_answer',
                value=hash_ if button == true_button else 'incorrect'
            )
        )

    keyboard.adjust(2, repeat=True)
    return keyboard, true_button
