from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ChatPermissions
from pydantic_settings import BaseSettings
from redis.asyncio import Redis as aioredis


class Settings(BaseSettings):

    telegram_bot_token: str
    telegram_bot_host: str
    dp: Dispatcher = Dispatcher(storage=MemoryStorage())
    bot_drop_pending_updates: bool = 1
    bot_request_timeout: int = 30
    bot_parse_mode: str = 'html'

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    captcha_answer_timeout: int = 30
    max_captcha_attempts: int = 5
    user_restrict_timeout: int = 60
    captcha_string_length: int = 5
    captcha_image_width: int = 200
    captcha_image_height: int = 60

    restricted_permissions: ChatPermissions = ChatPermissions(
        can_send_messages=False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_other_messages=True,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_manage_topics=False,
    )

    unrestricted_permissions: ChatPermissions = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True
    )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()

bot: Bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(
        parse_mode=settings.bot_parse_mode,
    )
)

redis_url = (
    f'redis://:{settings.redis_password}@{settings.redis_host}:'
    f'{settings.redis_port}/{settings.redis_db}'
)
redis_client: aioredis = aioredis.from_url(redis_url)
webhook_path = f'/bot/{settings.telegram_bot_token}'
webhook_url = f'{settings.telegram_bot_host}{webhook_path}'
