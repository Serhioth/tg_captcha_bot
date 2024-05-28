import asyncio

from aiogram import F, types, Router
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
    KICKED,
    LEFT
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError

from bot.callbacks.callback_fabs import CaptchaCallback
from bot.core.config import settings
from bot.core.configure_logging import logger
from bot.states.user_join_states import UserJoinStates
from bot.keyboards.captcha.captcha_keyboard_fabs import CaptchaFactory
from bot.keyboards.captcha.keyboards import ImageCaptcha
from bot.translations.ru.user_join_messages import (
    USER_JOIN_MESSAGE,
)
from bot.utils.handlers import (
    ban_user,
    check_user_attempts_is_over,
    protect_username,
    reset_user_attempts_number
)
from bot.utils.repositories import (
    increment_daily_failed_captcha_messages,
    increment_daily_passed_captcha_messages
)


router = Router()


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def on_user_join(
    event: types.ChatMemberUpdated,
    state: FSMContext,
):
    """Функция для обработки запроса на вступление в чат."""

    attempts_is_over = await check_user_attempts_is_over(
        user_id=event.new_chat_member.user.id,
    )

    if attempts_is_over:
        await state.set_state(UserJoinStates.attempts_limit_reached)
        await increment_daily_failed_captcha_messages()
        await ban_user(
            bot=event.bot,
            chat_id=event.chat.id,
            user_id=event.new_chat_member.user.id,
            state=state
        )
        return

    await state.set_state(UserJoinStates.waiting_for_answer)

    if event.from_user.id in event.chat.get_administrators():
        return

    if event.new_chat_member.status not in ('member', 'restricted'):
        return

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

    captcha = CaptchaFactory.get_captcha()

    await state.update_data(
        captcha=captcha
    )

    # Здесь собственный метод ответа, так как возвращаем картинку.
    if isinstance(captcha, ImageCaptcha):
        message = await event.answer_photo(
            photo=captcha.captcha,
            caption=USER_JOIN_MESSAGE.format(
                username=user_full_name,
                captcha_message=captcha.create_captcha_message()
            ),
            reply_markup=captcha.generate_captcha_keyboard().as_markup(),
            protect_content=True,
        )
    else:
        message = await event.answer(
            text=USER_JOIN_MESSAGE.format(
                username=user_full_name,
                captcha_message=captcha.create_captcha_message()
            ),
            reply_markup=captcha.generate_captcha_keyboard().as_markup(),
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


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=KICKED >> LEFT,
    ),
)
async def on_user_left(
    event: types.ChatMemberUpdated,
):
    """
    Функция обнуляет счётчик попыток на вступление пользователя,
    если он был разбанен администратором или вышел из чата по
    собственной воле.
    """
    user_id = event.new_chat_member.user.id
    attempts_is_over = await check_user_attempts_is_over(
        user_id=user_id,
    )
    if attempts_is_over:
        logger.info('Количество попыток входа пользователя сброшено.')
        await reset_user_attempts_number(user_id=user_id)


@router.callback_query(
    CaptchaCallback.filter(F.description == 'captcha_answer'),
)
async def process_user_answer(
    callback: types.CallbackQuery,
    callback_data: CaptchaCallback,
    state: FSMContext
) -> None:
    """Функция для обработки ответа пользователя."""

    await state.set_state(UserJoinStates.process_answer)

    user_full_name = protect_username(callback.from_user.full_name)

    state_data = await state.get_data()
    target_user_id = state_data.get('target_user_id')

    if target_user_id != callback.from_user.id:
        return

    captcha = state_data.get('captcha')

    if captcha.validate_captcha(callback_data.value):
        await callback.message.chat.restrict(
            user_id=callback.from_user.id,
            permissions=settings.unrestricted_permissions,
            use_independent_chat_permissions=True
        )
        await increment_daily_passed_captcha_messages()
        logger.info(
            f'Заявка пользователя {user_full_name} одобрена.'
        )
        await reset_user_attempts_number(user_id=callback.from_user.id)

        await callback.message.delete()
        await state.clear()

        return

    else:
        logger.info(
            f'Заявка пользователя {user_full_name} отклонена.'
        )

        await callback.message.delete()

        await increment_daily_failed_captcha_messages()
        await ban_user(
            bot=callback.bot,
            state=state,
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            kick=True
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

        logger.info(
            f'Заявка пользователя {user_full_name} завершена по таймауту.'
        )

        try:
            await message.delete()
            await increment_daily_failed_captcha_messages()

            await ban_user(
                bot=event.bot,
                chat_id=chat_id,
                user_id=user_id,
                kick=True
            )
            return
        except TelegramAPIError:
            return
