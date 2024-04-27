import logging
import sys


def configure_logging():
    """Утилита для настройки логгирования в приложении."""

    logger = logging.getLogger('Captcha Bot Logger')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


if not logging.getLogger().handlers:
    logger = configure_logging()
else:
    logger = logging.getLogger(__name__)
