from datetime import datetime as dt
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from bot.core.constants import BASE_DIR


def configure_logging():
    """Утилита для настройки логгирования в приложении."""

    now = dt.now().strftime('%d.%m.%Y_%H:%M:%S')

    logger = logging.getLogger('Captcha Bot Logger')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.INFO)


    logs_output_path = os.path.join(
            BASE_DIR.parent,
            'logs',
            f'{logger.name}_{now}'
        )

    os.makedirs(logs_output_path, exist_ok=True)

    rotating_file_handler = RotatingFileHandler(
        logs_output_path,
        maxBytes=50000000,
        backupCount=5,
        encoding='utf-8'
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    stream_handler.setFormatter(formatter)
    rotating_file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(rotating_file_handler)

    return logger


if not logging.getLogger().handlers:
    logger = configure_logging()
else:
    logger = logging.getLogger(__name__)
