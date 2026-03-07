from aiogram import types, F

from constants import ABOUT_US_TEXT
from routers import about_us_router


@about_us_router.message(F.text.contains("О нас"))
async def get_about_us(message: types.Message) -> None:
    await message.answer(
        text=ABOUT_US_TEXT,
        parse_mode="html",
    )
