from aiogram import types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constants import BASE_ADJUST
from routers import main_menu_router
from users.services import user_info


@main_menu_router.message((F.text == "🏠 Меню"))
@main_menu_router.message(Command("menu"))
async def menu(message: types.Message) -> None:
    builder = ReplyKeyboardBuilder()
    for button in [
        types.KeyboardButton(text="📅 Мероприятия"),
        types.KeyboardButton(text="🛍️ Магазин"),
        types.KeyboardButton(text="💵 Баланс"),
        types.KeyboardButton(text="ℹ️ О нас")
    ]:
        builder.add(button)

    user = await user_info(message.from_user.id)
    if user["is_admin"]:
        builder.add(types.KeyboardButton(text="👥 Пользователи"))
    builder.adjust(BASE_ADJUST)

    await message.answer("Главное меню:", reply_markup=builder.as_markup(resize_keyboard=True))
