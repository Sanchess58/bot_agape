from aiogram import types, F

from constants import ABOUT_US_TEXT, MENU_BUTTON_TEXT
from routers import about_us_router


@about_us_router.message(F.text.contains("О нас"))
async def get_about_us(message: types.Message):
    await message.answer(
        text=ABOUT_US_TEXT,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=MENU_BUTTON_TEXT)]],
            resize_keyboard=True,
        )
    )
