import base64
import hashlib


def generate_hash(
    tg_id: int,
    chat_id: int,
) -> str:
    """
    Функция для генерации хэша из телеграм айди
    пользователя и телеграм айди чата.
    """

    combined_string = f"{tg_id}{chat_id}"
    hashed_value = hashlib.sha256(combined_string.encode()).digest()
    short_hash = base64.b64encode(hashed_value).decode()[:10]

    return short_hash
