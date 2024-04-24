import asyncio

from aiogram import Bot, F, types, Router
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
)
from aiogram.fsm.context import FSMContext
from aiogram.handlers.chat_member import ChatMemberHandler

from bot.callbacks.callback_fabs import UserJoinCallback
from bot.core.configure_logging import logger
from bot.core.constants import (
    ANSWER_TIMEOUT,
    GROUP_ADMINSTRATOR_IDS,
    RESTRICTED_PERMISSIONS,
    UNRESTRICTED_PERMISSIONS
)
from bot.filters.is_allowed_group_filter import (
    IsAllowedGroupEventFilter
)
from bot.FSM_states.user_join_states import UserJoinStates
from bot.utils.async_timer import AsyncTimer
from bot.utils.handlers_utils import (
    check_user_id,
    protect_username,
    ban_user
)
from bot.translations.ru.user_join_messages import (
    NON_TARGET_USER_MESSAGE,
    USER_JOIN_MESSAGE,
    USER_TIMEOUT_MESSAGE,
    USER_CORRECT_ANSWER_MESSAGE,
    USER_INCORRECT_ANSWER_MESSAGE
)
from bot.keyboards.user_join_handlers_keyboards.captcha_keyboard import (
    generate_captcha_keyboard
)
from bot.utils.async_timer import AsyncTimer


router = Router()

router.chat_member.filter(IsAllowedGroupEventFilter())


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def on_user_join(
    event: types.ChatMemberUpdated,
    state: FSMContext,
):
    """Функция для обработки запроса на вступление в чат."""

    await state.set_state(UserJoinStates.waiting_for_answer)

    if event.from_user.id in GROUP_ADMINSTRATOR_IDS:
        return None

    if event.new_chat_member.status not in ('member', 'restricted'):
        return None

    user_id = event.new_chat_member.user.id
    user_full_name = protect_username(event.new_chat_member.user.full_name)

    logger.info(f'Статус пользователя {event.new_chat_member.status}')

    await state.update_data(
        target_user_id=user_id,
        target_user_full_name=user_full_name
    )

    logger.info(
        f'Пользователь {user_full_name} '
        'подал заявку на вступление в группу.'
    )

    keyboard, true_button = generate_captcha_keyboard()

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
        permissions=RESTRICTED_PERMISSIONS,
        use_independent_chat_permissions=True
    )

    await asyncio.sleep(ANSWER_TIMEOUT)

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
        return


@router.callback_query(
    UserJoinCallback.filter(
        F.value == 'correct'
    )
)
async def process_correct_answer(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Хэндлер для обработки ответа пользователя."""

    await state.set_state(UserJoinStates.process_correct_answer)

    user_full_name = protect_username(callback.from_user.full_name)

    await check_user_id(
        callback=callback,
        state=state,
        alert_message=NON_TARGET_USER_MESSAGE.format(
            username=user_full_name
        )
    )

    await callback.message.chat.restrict(
        user_id=callback.from_user.id,
        permissions=UNRESTRICTED_PERMISSIONS,
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


@router.callback_query(
    UserJoinCallback.filter(
        F.value == 'incorrect'
    )
)
async def process_incorrect_answer(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Хэндлер для обработки неверного ответа пользователя."""

    await state.set_state(UserJoinStates.process_incorrect_answer)

    user_full_name = protect_username(
        callback.from_user.full_name
    )

    await check_user_id(
        callback=callback,
        state=state,
        alert_message=NON_TARGET_USER_MESSAGE.format(
            username=protect_username(
                user_full_name
            )
        )
    )

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
