from aiogram import types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constants import MENU_BUTTON_TEXT
from routers import users_router
from .services import get_users, user_info
from .utils import format_user


@users_router.message(F.text == "💵 Баланс")
async def user_balance(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    user = await user_info(message.from_user.id)
    await message.answer(text=f"Баланс: {user['balance']} 💵", reply_markup=builder.as_markup(resize_keyboard=True))


@users_router.message(F.text == "👥 Пользователи")
async def users(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    users = await get_users(message.from_user.id)
    message_text = ""
    for user in users:
        message_text += format_user(user)
    await message.answer(
        text=message_text,
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="html",
        )
