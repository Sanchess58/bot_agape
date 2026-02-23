from aiogram import types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constants import MENU_BUTTON_TEXT
from shops.utils import format_product
from shops.requests import get_products
from routers import shops_router


@shops_router.message(F.text == "🛍️ Магазин")
async def products(message: types.Message):
    products = await get_products(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    try:
        if not products:
            return await message.answer("Совсем скоро в магазине будут товары за монетки")

        for product in products: 
            await message.answer_photo(
                photo=product["photo"],
                caption=format_product(),
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
    except Exception:
        await message.answer("⚠️ Ошибка при получении товаров.\n Обратитесь к @sancheser")
