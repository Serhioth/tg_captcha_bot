import random
from string import ascii_letters, digits
import base64
import hashlib


def generate_hash() -> str:
    """Функция для генерации случайного хэша."""

    random_sample = "".join(
        random.sample(ascii_letters + digits, 10)
    )
    hashed_value = hashlib.sha256(random_sample.encode()).digest()
    short_hash = base64.b64encode(hashed_value).decode()[:10]

    return short_hash
