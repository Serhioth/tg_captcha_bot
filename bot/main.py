from contextlib import asynccontextmanager
from datetime import datetime as dt

from aiogram import types
from aiogram_dialog import setup_dialogs
from fastapi import FastAPI
import uvicorn

from bot.core.config import bot, settings, webhook_path, webhook_url
from bot.core.configure_logging import logger
from bot.handlers import (
    chat_member_router,
    service_router,
    commands_router,
    statistics_dialog,
)


DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

now = dt.now().strftime(DATETIME_FORMAT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""

    logger.info(f'Бот запущен в {now}.')
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        request_timeout=30,
        allowed_updates=["message",
                         "callback_query",
                         "inline_query",
                         "chat_member"]
    )
    settings.dp.include_routers(
        chat_member_router,
        service_router,
        commands_router,
        statistics_dialog,
    )
    setup_dialogs(settings.dp)
    logger.info(f'Диспетчер запущен в {now}.')

    yield

    await bot.delete_webhook(
        drop_pending_updates=True,
    )
    logger.info(f'Бот остановлен в {now}.')


app = FastAPI(lifespan=lifespan)


@app.post(path=webhook_path)
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""

    telegram_update = types.Update(**update)
    await settings.dp.feed_update(bot=bot,
                                  update=telegram_update)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8181)
