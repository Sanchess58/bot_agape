import asyncio

from aiogram import types
from aiogram.filters import Command

from constants import  WELCOME_TEXT
from main import bot, dp
import about_us.routers as about_us
import users.registration_users as registration_users
import users.routers as users
import events.routers as events
import shops.routes as shops
import main_menu


async def main():
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Регистрация")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer(WELCOME_TEXT, reply_markup=keyboard)

if __name__ == "__main__":
    asyncio.run(main())
