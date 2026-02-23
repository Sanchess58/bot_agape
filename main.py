from aiogram import Bot, Dispatcher

from constants import BOT_TOKEN
from routers import (
    about_us_router,
    events_router,
    main_menu_router,
    shops_router,
    users_router,
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    about_us_router,
    users_router,
    events_router,
    shops_router,
    main_menu_router,
)
