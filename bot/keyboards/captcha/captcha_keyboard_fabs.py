import random

from bot.keyboards.captcha.keyboards import (
    EmojiCaptcha,
    MathCaptcha,
    ImageCaptcha,
    QuestionCaptcha
)
from bot.translations.ru.captcha_messages import (
    EMOJI_CAPTCHA_MESSAGE,
    MATH_CAPTCHA_MESSAGE,
    IMAGE_CAPTCHA_MESSAGE,
    QUESTION_CAPTCHA_MESSAGE
)
from bot.utils.captcha import (
    generate_emoji_captcha,
    generate_math_captcha,
    generate_image_captcha,
    generate_question_captcha
)


class CaptchaFactory:
    """Класс для выбора случайного метода генерации каптчи."""

    @staticmethod
    def get_captcha():
        captcha_methods = [
            EmojiCaptcha,
            MathCaptcha,
            ImageCaptcha,
            QuestionCaptcha
        ]

        chosen_method = random.choice(captcha_methods)

        if chosen_method == EmojiCaptcha:
            return chosen_method(
                generate_emoji_captcha,
                EMOJI_CAPTCHA_MESSAGE
            )
        elif chosen_method == MathCaptcha:
            return chosen_method(
                generate_math_captcha,
                MATH_CAPTCHA_MESSAGE
            )
        elif chosen_method == ImageCaptcha:
            return chosen_method(
                generate_image_captcha,
                IMAGE_CAPTCHA_MESSAGE
            )
        elif chosen_method == QuestionCaptcha:
            return chosen_method(
                generate_question_captcha,
                QUESTION_CAPTCHA_MESSAGE
            )
