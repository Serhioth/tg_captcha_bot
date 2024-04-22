from .callback_query_handlers.private_admin_callback_handlers import router as private_admin_callback_router  # noqa
from .command_handlers.group_admin_command_handlers import router as group_admin_command_router  # noqa
from .command_handlers.private_admin_command_handlers import router as private_admin_command_router  # noqa
from .event_handlers.chat_member_handlers import router as event_router  # noqa
from .message_handlers.private_admin_messages_handlers import router as private_admin_messages_router  # noqa
