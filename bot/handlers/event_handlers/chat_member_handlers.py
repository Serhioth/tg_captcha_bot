import asyncio

from aiogram import F, types, Router
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
)
from aiogram.fsm.context import FSMContext

from bot.callbacks.callback_fabs import UserJoinCallback
from bot.core.config import settings
from bot.core.configure_logging import logger
from bot.FSM_states.user_join_states import UserJoinStates
from bot.keyboards.user_join_handlers_keyboards.captcha_keyboard import (
    generate_captcha_keyboard
)

from bot.translations.ru.user_join_messages import (
    NON_TARGET_USER_MESSAGE,
    USER_JOIN_MESSAGE,
    USER_TIMEOUT_MESSAGE,
    USER_CORRECT_ANSWER_MESSAGE,
    USER_INCORRECT_ANSWER_MESSAGE
)
from bot.utils.handlers_utils import (
    protect_username,
    ban_user
)
from bot.utils.hash import generate_hash


router = Router()


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def on_user_join(
    event: types.ChatMemberUpdated,
    state: FSMContext,
):
    """Функция для обработки запроса на вступление в чат."""

    await state.set_state(UserJoinStates.waiting_for_answer)

    if event.from_user.id in event.chat.get_administrators():
        return None

    if event.new_chat_member.status not in ('member', 'restricted'):
        return None

    user_id = event.new_chat_member.user.id
    user_full_name = protect_username(event.new_chat_member.user.full_name)

    logger.info(f'Статус пользователя {event.new_chat_member.status}')

    await state.update_data(
        target_user_id=user_id
    )

    logger.info(
        f'Пользователь {user_full_name} '
        'подал заявку на вступление в группу.'
    )

    keyboard, true_button = generate_captcha_keyboard(
        chat_id=event.chat.id,
        user_id=user_id
    )

    message = await event.answer(
        text=USER_JOIN_MESSAGE.format(
            username=user_full_name,
            symbol=true_button
        ),
        reply_markup=keyboard.as_markup(),
        protect_content=True
    )

    await event.chat.restrict(
        user_id=user_id,
        permissions=settings.restricted_permissions,
        use_independent_chat_permissions=True,
    )

    return asyncio.create_task(
        process_user_timeout(
            state=state,
            message=message,
            event=event,
        )
    )


@router.callback_query(
    UserJoinCallback.filter(F.description == 'captcha_answer'),
)
async def process_user_answer(
    callback: types.CallbackQuery,
    state: FSMContext
) -> None:
    """Функция для обработки ответа пользователя."""

    user_full_name = protect_username(callback.from_user.full_name)

    state_data = await state.get_data()
    target_user_id = state_data.get('target_user_id')

    if target_user_id is None:
        await callback.answer(
            text=NON_TARGET_USER_MESSAGE.format(
                username=user_full_name
            ),
            show_alert=True
        )
        return None

    correct_answer = generate_hash(
        callback.message.chat.id,
        target_user_id
    )

    if callback.data == correct_answer:
        await callback.message.chat.restrict(
            user_id=callback.from_user.id,
            permissions=settings.unrestricted_permissions,
            use_independent_chat_permissions=True
        )

        logger.info(
            f'Заявка пользователя {user_full_name} одобрена.'
        )
        await callback.message.answer(
            text=USER_CORRECT_ANSWER_MESSAGE.format(
                username=user_full_name
            )
        )

        await callback.message.delete()
        await state.clear()

        return

    else:
        logger.info(
            f'Заявка пользователя {user_full_name} отклонена.'
        )
        await callback.message.answer(
            text=USER_INCORRECT_ANSWER_MESSAGE.format(
                username=user_full_name
            )
        )

        await callback.message.delete()

        await ban_user(
            bot=callback.bot,
            state=state,
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id
        )
        return


async def process_user_timeout(
    state: FSMContext,
    event: types.ChatMemberUpdated,
    message: types.Message,
):
    """Функция для забанивания пользователя по таймауту. """

    await asyncio.sleep(settings.captcha_answer_timeout)

    current_state = await state.get_state()

    if current_state == UserJoinStates.waiting_for_answer:

        user_full_name = protect_username(
            event.new_chat_member.user.full_name
        )
        user_id = event.new_chat_member.user.id
        chat_id = event.chat.id

        await event.answer(
            text=USER_TIMEOUT_MESSAGE.format(
                username=user_full_name
            )
        )

        logger.info(
            f'Заявка пользователя {user_full_name} завершена по таймауту.'
        )

        await message.delete()

        await ban_user(
            bot=event.bot,
            chat_id=chat_id,
            user_id=user_id
        )
    else:
        return
