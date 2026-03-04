from aiogram import types, F

from routers import users_router
from .services import get_users, user_info
from .utils import format_user


@users_router.message(F.text == "💵 Баланс")
async def user_balance(message: types.Message):
    user = await user_info(message.from_user.id)
    await message.answer(text=f"Баланс: {user['balance']} 💵")


@users_router.message(F.text == "👥 Пользователи")
async def users(message: types.Message):
    users = await get_users(message.from_user.id)
    last_index = len(users)

    message_text = ""
    for i, user in enumerate(users, start=1):
        message_text += format_user(user)
        if i % 5 == 0 or i == last_index:
            await message.answer(
                text=message_text,
                parse_mode="html",
            )
            message_text = ""
