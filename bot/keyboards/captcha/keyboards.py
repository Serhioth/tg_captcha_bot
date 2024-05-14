from typing import Callable

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import CaptchaCallback
from bot.keyboards.captcha.captcha_base_interface import CaptchaInterface


class BaseCaptcha(CaptchaInterface):
    """Каптча, работающая с эмодзи."""

    def __init__(
        self,
        captcha_generator: Callable,
        captcha_message: str,
    ):
        # captcha_generator - одна из представленных
        # в утилитах функций для генерации капчи.
        # Всегда возвращает captcha - испытание, answer - правильный ответ
        # и choices - словарь с ответами для выбора.
        self.keyboard = InlineKeyboardBuilder()
        self.captcha_generator = captcha_generator
        self.captcha, self.answer, self.choices = self.captcha_generator()
        self.captcha_message = captcha_message

    def generate_captcha_keyboard(self) -> InlineKeyboardBuilder:
        """
        Конструктор клавиатуры с вариантами ответа.
        Возвращает сгенерированную клавиатуру.
        """

        buttons = []

        for key, value in self.choices.items():
            buttons.append({
                'text': str(key),
                'callback_data': CaptchaCallback(
                    description='captcha_answer',
                    value=value
                )
            })

        for button in buttons:
            self.keyboard.button(**button)

        self.keyboard.adjust(2, repeat=True)
        return self.keyboard

    def create_captcha_message(self):
        """Метод для создания сообщения с каптчей."""
        return self.captcha_message.format(
            captcha=self.captcha
        )

    def validate_captcha(self, user_answer: str) -> bool:
        """Метод для проверки ответа пользователя."""
        correct_hash = self.choices.get(self.answer)
        return user_answer == correct_hash


class EmojiCaptcha(BaseCaptcha):
    """Каптча, работающая с эмодзи."""

    def __init__(
        self,
        captcha_generator: Callable,
        captcha_message: str,
    ):
        super().__init__(captcha_generator, captcha_message)


class MathCaptcha(BaseCaptcha):
    """Каптча, работающая с математическими примерами."""

    def __init__(
        self,
        captcha_generator: Callable,
        captcha_message: str,
    ):
        super().__init__(captcha_generator, captcha_message)


class ImageCaptcha(BaseCaptcha):
    """Каптча, генерирующая изображение."""

    def __init__(
        self,
        captcha_generator: Callable,
        captcha_message: str,
    ):
        super().__init__(captcha_generator, captcha_message)

    def create_captcha_message(self):
        return self.captcha_message


class QuestionCaptcha(BaseCaptcha):
    """Каптча, работающая с ответами на вопросы."""

    def __init__(
        self,
        captcha_generator: Callable,
        captcha_message: str,
    ):
        super().__init__(captcha_generator, captcha_message)
