from aiogram.filters.callback_data import CallbackData


class BuyShopItemCallback(CallbackData, prefix="buy_shopitem"):
    shop_item_id: int
    shop_item_name: str
