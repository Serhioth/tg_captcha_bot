import math

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.callback_fabs import (
    PaginationCallback
)
from bot.core.constants import USERS_PER_PAGE
from bot.core.db_config import DatabaseManager


async def generate_banned_users_keyboard(page=1):
    """
    Клавиатура списка забаненных пользователей.
    Генерируется динамически из записей в БД.
    Поддерживает динамическую пагинацию.
    """

    keyboard = InlineKeyboardBuilder()
    db_manager = DatabaseManager()
    db = await db_manager.get_db()
    collection = db.banned_users

    all_users = await collection.find().to_list(length=None)

    if not all_users:
        return None

    if len(all_users) <= USERS_PER_PAGE:
        for user in all_users:
            keyboard.button(
                text=user['full_name'],
                callback_data=PaginationCallback(
                    description='banned_users',
                    value=user['_id']
                )
            )
        keyboard.adjust(1, repeat=True)

        return keyboard.as_markup()

    number_of_pages = math.ceil(len(all_users) / USERS_PER_PAGE)

    banned_users = [all_users[(page - 1) * USERS_PER_PAGE]]

    for user in banned_users:
        keyboard.button(
            text=user['full_name'],
            callback_data=PaginationCallback(
                description='banned_users',
                value=user['_id']
            )
        )
        keyboard.adjust(1)

    previous_page_button = keyboard.button(
        text="⏪",
        callback_data=PaginationCallback(
            description='page',
            value=page - 1
        )
    )

    first_page_button = keyboard.button(
        text="⏮",
        callback_data=PaginationCallback(
            description='page',
            value=1
        )
    )

    next_page_button = keyboard.button(
        text="⏩",
        callback_data=PaginationCallback(
            description='page',
            value=page + 1
        )
    )

    last_page_button = keyboard.button(
        text="⏭",
        callback_data=PaginationCallback(
            description='page',
            value=number_of_pages
        )
    )

    page_counter = keyboard.button(
        text=f'{page}/{number_of_pages}',
        callback_data=PaginationCallback(
            description='page_counter',
            value='page_counter'
        )
    )

    cancel_button = keyboard.button(
        text='Отмена',
        callback_data=PaginationCallback(
            description='cancel',
            value='cancel'
        )
    )

    if page == 1:
        keyboard.row(
            page_counter,
            cancel_button
        )

    elif page == number_of_pages:
        keyboard.row(
            previous_page_button,
            first_page_button,
            page_counter,
            cancel_button
        )

    elif page > 1 and page < number_of_pages:
        keyboard.row(
            previous_page_button,
            first_page_button,
            page_counter,
            next_page_button,
            last_page_button,
            cancel_button
        )

    return keyboard.as_markup()
