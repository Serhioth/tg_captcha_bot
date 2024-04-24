import os
from pathlib import Path

from aiogram.types import ChatPermissions
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_HOST = os.getenv('TELEGRAM_BOT_HOST')
TELEGRAM_GROUP_ID = int(os.getenv('TELEGRAM_GROUP_ID'))
GROUP_ADMINSTRATOR_IDS = [
    int(admin_id) for admin_id in os.getenv(
        'GROUP_ADMINSTRATOR_IDS').split(',')
]
ANSWER_TIMEOUT = 30
RESTRICT_TIMEOUT = 60

RESTRICTED_PERMISSIONS = ChatPermissions(
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

UNRESTRICTED_PERMISSIONS = ChatPermissions(
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
