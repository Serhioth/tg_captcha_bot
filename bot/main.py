from contextlib import asynccontextmanager
from datetime import datetime as dt

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
import uvicorn

from bot.core.config import settings
from bot.core.configure_logging import logger
from bot.handlers import (
    event_router,
    group_admin_command_router,
)


DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
WEBHOOK_PATH = f'/bot/{settings.telegram_bot_token}'
WEBHOOK_URL = f'{settings.telegram_bot_host}{WEBHOOK_PATH}'

now = dt.now().strftime(DATETIME_FORMAT)

bot = Bot(
    token=settings.telegram_bot_token,
    parse_mode='HTML'
)
dp = Dispatcher(storage=MemoryStorage())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""

    logger.info(f'Бот запущен в {now}.')
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True,
        request_timeout=30,
        allowed_updates=["message",
                         "callback_query",
                         "inline_query",
                         "chat_member"]
    )
    dp.include_routers(
        event_router,
        group_admin_command_router
    )
    logger.info(f'Диспетчер запущен в {now}.')

    yield

    await bot.delete_webhook(
        drop_pending_updates=True,
    )
    logger.info(f'Бот остановлен в {now}.')


app = FastAPI(lifespan=lifespan)


@app.post(path=WEBHOOK_PATH)
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""

    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot,
                         update=telegram_update)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8181)
