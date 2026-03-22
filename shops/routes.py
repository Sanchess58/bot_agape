import logging

import httpx
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import base64_to_file
from shops.callbacks import BuyShopItemCallback
from shops.requests import buy_product_request, get_products
from shops.utils import format_product
from routers import shops_router


@shops_router.message(F.text == "🛍️ Магазин")
async def products(message: types.Message) -> None | types.Message:
    return await message.answer("🚧 Магазин на реконструкции")
    # products = await get_products(message.from_user.id)

    # try:
    #     if not products:
    #         return await message.answer("Совсем скоро в магазине будут товары за монетки")

    #     for product in products:
    #         builder = InlineKeyboardBuilder()
    #         builder.button(
    #             text="✅ Купить",
    #             callback_data=BuyShopItemCallback(shop_item_id=product["id"]).pack()
    #         )

    #         photo_file = await base64_to_file(product)

    #         await message.answer_photo(
    #             photo=photo_file,
    #             caption=format_product(product),
    #             reply_markup=builder.as_markup(),
    #             parse_mode="HTML"
    #         )

    # except Exception as e:
    #     logging.error(e)
    #     return await message.answer("⚠️ Ошибка при получении товаров.\n Обратитесь к @sancheser")


@shops_router.callback_query(BuyShopItemCallback.filter())
async def buy_product(callback: types.CallbackQuery, callback_data: BuyShopItemCallback) -> None | types.Message:
    try:
        response = await buy_product_request(
            telegram_id=callback.from_user.id,
            product_id=callback_data.shop_item_id,
        )
        await callback.message.delete()
        if response.status_code == httpx.codes.BAD_REQUEST:
            return await callback.answer(response.json()["detail"])
        await callback.message.answer(
            f"Поздравляем с покупкой 🎉\nЗа подробностями обращайтесь к @sancheser",
            parse_mode="html",
        )
    except Exception as err:
        logging.error(err)
        return await callback.message.answer("⚠️ Ошибка при покупке.\n Обратитесь к @sancheser")
