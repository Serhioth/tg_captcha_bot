import io
import random
from string import ascii_letters, digits
import base64
import hashlib

from aiogram.types import BufferedInputFile
from PIL import Image, ImageDraw, ImageFont

from bot.core.config import settings
from bot.translations.ru.captcha_questions import captcha_questions


def generate_hash(sample: str = None) -> str:
    """Функция для генерации случайного хэша."""
    if not sample:
        sample = "".join(
            random.sample(ascii_letters + digits, 10)
        )
    hashed_value = hashlib.sha256(sample.encode()).digest()
    short_hash = base64.b64encode(hashed_value).decode()[:10]

    return short_hash


def shuffle_answer_choices(
    answer_choices: dict[str, str],
    correct_answer: str,
    correct_hash: str
):
    """Функция для перемешивания вариантов ответа на каптчу."""
    answer_choices_list = list(answer_choices.items())
    answer_choices_list.append((correct_answer, correct_hash))
    random.shuffle(answer_choices_list)

    answer_choices = {}

    for answer in answer_choices_list:
        answer_choices[answer[0]] = answer[1]

    return answer_choices


def generate_math_example() -> tuple[str, str]:
    """Генерирует математические примеры с целочисленным ответом."""
    operators = ['+', '-', '*', '/']

    while True:
        num_1 = random.randint(1, 10)
        num_2 = random.randint(1, 10)
        operator_1 = random.choice(operators)
        operator_2 = random.choice(operators)

        example = f"{num_1} {operator_1} {num_2} {operator_2} {num_1}"
        try:
            result = eval(example)
            if isinstance(result, int):
                correct_answer = str(result)
                break
        except ZeroDivisionError:
            pass

    return example, correct_answer


def generate_emoji_captcha():
    """Функция для генерирования случайных наборов эмоджи."""
    emoji_choices = ['🦑', '🐙', '🦕', '🦖', '🦎', '🐍',
                     '🪰', '🪲', '🪳', '🦟', '🦗', '🕷',
                     '🦋', '🐛', '🪱', '🐝', '🫎', '🦄',
                     '🪿', '🦆', '🐦‍⬛️', '🦅', '🦉', '🦇',
                     '🐳', '🐬', '🐟', '🐠', '🐡', '🦀']

    chosen_emojis = random.sample(emoji_choices, 4)
    captcha = correct_answer = random.choice(chosen_emojis)
    correct_hash = generate_hash()

    answer_choices = {}

    for choice in chosen_emojis:
        if choice != correct_answer:
            answer_choices[choice] = generate_hash()

    answer_choices = shuffle_answer_choices(
        answer_choices, correct_answer, correct_hash
    )
    return captcha, correct_answer, answer_choices


def generate_math_captcha() -> tuple[str, int, list[int]]:
    """Функция для генерирования данных для математической каптчи."""
    captcha, correct_answer = generate_math_example()
    correct_hash = generate_hash()

    answer_choices = {}

    while len(answer_choices) < 3:
        random_answer = random.randint(-100, 100)
        if random_answer != correct_answer:
            answer_choices[random_answer] = generate_hash()

    answer_choices = shuffle_answer_choices(
        answer_choices, correct_answer, correct_hash
    )

    return captcha, correct_answer, answer_choices


def generate_random_string() -> str:
    """Функция для генерации случайной строки."""
    random_string = "".join(
        random.sample(ascii_letters + digits, settings.captcha_string_length)
    )
    return random_string


def get_random_image_coordinate(
    width: int = settings.captcha_image_width,
    height: int = settings.captcha_image_height,
) -> tuple[int, int]:
    """Функция для получения случайно точки в пределах изображения."""
    x = random.randint(5, width)
    y = random.randint(5, height)
    return x, y


def generate_image_captcha() -> tuple[io.BytesIO, str, list[str]]:
    """
    Функция для генерации случайного изображения для каптчи.
    Возвращает изображение, правильный ответ и список ответов
    для клавиатуры.
    """
    correct_answer = generate_random_string()
    correct_hash = generate_hash()
    captcha_image = Image.new("RGB", (200, 60), (255, 255, 255))
    draw = ImageDraw.Draw(captcha_image)

    text_colors = [
        "black",
        "red",
        "blue",
        "green",
    ]
    line_colors = [
        (64, 107, 76),
        (0, 87, 128),
        (0, 3, 82),
        (191, 0, 255),
        (72, 189, 0),
        (189, 107, 0),
        (189, 41, 0)
    ]
    text_color = random.choice(text_colors)
    line_color = random.choice(line_colors)
    font = ImageFont.truetype(
        "bot/keyboards/captcha/fonts/Onest-Regular.ttf",
        40
    )
    text_x_position = 35
    text_y_position = 10

    draw.text(
        (text_x_position, text_y_position),
        correct_answer,
        fill=text_color,
        font=font
    )

    for _ in range(5, random.randrange(6, 10)):
        draw.line(
            [get_random_image_coordinate(), get_random_image_coordinate()],
            fill=line_color,
            width=random.randrange(1, 3),
        )

    for _ in range(10, random.randrange(11, 20)):
        draw.point(
            get_random_image_coordinate(),
            fill=random.choice(text_colors),
        )

    image_buffer = io.BytesIO()
    captcha_image.save(image_buffer, format='PNG')
    image_data = image_buffer.getvalue()

    captcha = BufferedInputFile(image_data, "captcha.png")

    answer_choices = {}

    for _ in range(3):
        random_answer = generate_random_string()
        if random_answer != correct_answer:
            answer_choices[random_answer] = generate_hash()

    answer_choices = shuffle_answer_choices(
        answer_choices, correct_answer, correct_hash
    )

    return captcha, correct_answer, answer_choices


def generate_question_captcha() -> tuple[str, str, dict[str, str]]:
    """Генерирует каптчу с вопросами и ответами."""
    question_data = random.choice(list(captcha_questions.items()))
    question, answers = question_data[0], question_data[1]

    correct_answer = next(key for key, value in answers.items() if value)
    correct_hash = generate_hash()

    answer_choices = {}
    for key, value in answers.items():
        if key != correct_answer:
            answer_choices[key] = generate_hash()

    answer_choices = shuffle_answer_choices(
        answer_choices, correct_answer, correct_hash
    )

    return question, correct_answer, answer_choices
