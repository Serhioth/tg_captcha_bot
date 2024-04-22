from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.FSM_states.unban_user_states import UnbanUserStates
from bot.utils.handlers_utils import (
    get_banned_users_collection,
    protect_username
)
from bot.keyboards.private_command_handlers_keyboards import (
    generate_confirm_keyboard
)
from bot.translations.ru.private_command_messages import (
    CANCEL_MESSAGE,
    CHOICE_SELECT_MESSAGE,
    INCORRECT_ID_MESSAGE,
    USER_NOT_FOUND_IN_DB_MESSAGE
)


router = Router()


@router.message(F.text.startswith('ID'), UnbanUserStates.id_unban)
async def get_id(message: types.Message,
                 state: FSMContext):

    user_full_name = protect_username(message.from_user.full_name)

    try:
        user_id = int(message.text.split('=', maxsplit=1)[1])
    except ValueError:
        await message.answer(
            text=INCORRECT_ID_MESSAGE.format(
                username=user_full_name
            )
        )
        return

    banned_users_colection = await get_banned_users_collection()
    user_data = await banned_users_colection.find_one({'_id': user_id})

    if user_data is None:
        await message.answer(
            text=USER_NOT_FOUND_IN_DB_MESSAGE.format(
                username=user_full_name
            )
        )
        return

    await state.update_data(user_id=user_data['_id'])

    await message.answer(
        text=CHOICE_SELECT_MESSAGE.format(
            username=user_full_name
        ),
        reply_markup=generate_confirm_keyboard()
    )


@router.message(F.text.startswith('Имя'), UnbanUserStates.full_name_unban)
async def get_full_name(message: types.Message,
                        state: FSMContext):

    user_full_name = protect_username(message.from_user.full_name)

    target_user_full_name = protect_username(
        message.text.split('=', maxsplit=1)[1]
    )

    banned_users_colection = await get_banned_users_collection()
    user_data = await banned_users_colection.find_one(
        {'full_name': target_user_full_name}
    )

    if user_data is None:
        await message.answer(
            text=USER_NOT_FOUND_IN_DB_MESSAGE.format(
                username=user_full_name
            )
        )
        return

    await state.update_data(user_id=user_data['_id'])

    await message.answer(
        text=CHOICE_SELECT_MESSAGE.format(
            username=user_full_name
        ),
        reply_markup=generate_confirm_keyboard()
    )


@router.message(
    F.text.casefold() == 'отмена',
    UnbanUserStates.full_name_unban
)
@router.message(
    F.text.casefold() == 'отмена',
    UnbanUserStates.id_unban
)
async def cancel_unban(message: types.Message,
                       state: FSMContext):

    await state.clear()

    await message.answer(
        text=CANCEL_MESSAGE
    )
