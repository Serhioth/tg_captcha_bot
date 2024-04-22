from aiogram import F, types, Router


docs_router = Router()


@docs_router.message(F.document)
async def docs_handler(message: types.Message):
    await message.answer(
        f"Файл {message.document} загружен"
    )
