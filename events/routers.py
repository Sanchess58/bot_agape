import calendar
import logging
import httpx
from datetime import datetime

from aiogram import types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from constants import DAY_OF_THE_WEEK, MENU_BUTTON_TEXT
from events.callbacks import ConfirmationUserEventCallback, GetUserEventCallback, RegisterEventCallback
from events.utils import builder_button_event_users, builder_info_register_button, format_event, generate_event_message
from events.requests import events, get_event, my_events, register_to_event, users_at_event, user_is_attended
from routers import events_router
from users.routers import get_users
from users.utils import format_user
from utils import get_name_weekday


@events_router.message(F.text == "📅 Мероприятия")
async def menu_events(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    builder.add(types.KeyboardButton(text="📅 Мои мероприятия"))
    builder.add(types.KeyboardButton(text="📅 Календарь мероприятий"))
    builder.adjust(3)

    await message.answer(text="Выберите действие:", reply_markup=builder.as_markup(resize_keyboard=True))


@events_router.message(F.text == "📅 Календарь мероприятий")
async def calendar_events(message: types.Message):
    year = datetime.now().year
    month = datetime.now().month

    _, days = calendar.monthrange(year, month)
    builder = ReplyKeyboardBuilder()

    first_date_month = datetime(year, month, 1).date().isoformat()
    last_date_month = datetime(year, month, days).date().isoformat()

    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    events_list = await events(message.from_user.id, date_from=first_date_month, date_to=last_date_month)
    if not events_list:
        return await message.answer("Мероприятий еще нет 😞 Загляните позже!")

    events_days = {datetime.fromisoformat(event["date_and_time"]).day for event in events_list}
    for day in events_days:
        builder.add(types.KeyboardButton(text=f"{day} {get_name_weekday(calendar.weekday(year, month, day))}"))
    builder.adjust(DAY_OF_THE_WEEK)

    await message.answer(text="Даты мероприятий:", reply_markup=builder.as_markup(resize_keyboard=True))


@events_router.message(F.text == "📅 Мои мероприятия")
async def my_events_router(message: types.Message):
    events = await my_events(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=MENU_BUTTON_TEXT))
    try:
        if not events:
            return await message.answer("Вы не зарегистрированы ни на одно мероприятие 😞")

        for ev in events: 
            await message.answer_photo(
                photo=ev["photo_url"],
                caption=format_event(ev),
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
    except Exception as e:
        await message.answer("⚠️ Ошибка при получении мероприятий!\nОбратитесь к @sancheser")
        logging.error(msg=e)


@events_router.message(F.text.regexp(r"^\d{1,2}\s"))
async def date_selected(message: types.Message):
    """
    Пользователь выбрал дату из календаря, отдаем мероприятия на этот день.
    """
    day = int(message.text.split()[0])
    now = datetime.now()
    selected_date = datetime(now.year, now.month, day).date().isoformat()

    events_list = await events(message.from_user.id, date_from=selected_date, date_to=selected_date)
    register_events = await my_events(message.from_user.id)

    try:
        for event in events_list:
            builder = InlineKeyboardBuilder()
            if (
                datetime.fromisoformat(event["date_and_time"]).date() >= datetime.now().date() and
                event["id"] not in [register_event["id"] for register_event in register_events]
            ):
                await builder_info_register_button(builder, event["id"], message.from_user.id, "✅ Зарегистрироваться")

            elif event["id"] in [register_event["id"] for register_event in register_events]:
                await builder_info_register_button(builder, event["id"], message.from_user.id, "✔️ Вы зарегистрированы!")

            await builder_button_event_users(builder, event["id"], message.from_user.id)
            await generate_event_message(builder, event, message)

    except Exception as e:
        await message.answer("⚠️ Ошибка при получении мероприятий!\nОбратитесь к @sancheser")
        logging.error(msg=e)


@events_router.callback_query(RegisterEventCallback.filter())
async def event_register(callback: types.CallbackQuery, callback_data: RegisterEventCallback):
    try:
        response = await register_to_event(callback.from_user.id, callback_data.event_id)
        if response.status_code == httpx.codes.BAD_REQUEST:
            await callback.answer("Вы уже зарегистрированы на мероприятие!")

        builder = InlineKeyboardBuilder()
        await builder_button_event_users(builder, callback_data.event_id, callback.message.from_user.id, "✔️ Вы зарегистрированы!")
        new_markup = builder.as_markup()

        current_markup_dict = callback.message.reply_markup.model_dump() if callback.message.reply_markup else None
        if current_markup_dict != new_markup.model_dump():
            await callback.message.edit_reply_markup(reply_markup=new_markup)

        await callback.answer("Вы зарегистрированы на мероприятие!")

    except Exception as e:
        await callback.answer("⚠️ Ошибка при регистрации!\nОбратитесь к @sancheser")
        logging.error(msg=e)


@events_router.callback_query(GetUserEventCallback.filter())
async def event_users(callback: types.CallbackQuery, callback_data: RegisterEventCallback):
    try:
        users_in_event = await users_at_event(callback.from_user.id, callback_data.event_id)
        attended_users = {eu["user_id"]: eu["attended"] for eu in users_in_event}
        event = await get_event(callback.from_user.id, callback_data.event_id)
        users = await get_users(callback.from_user.id, ids=[eu for eu in attended_users.keys()])

        attended = "✅ Присутствовал"
        not_attended = "❌ Отсутствовал"

        for user in users:
            user_id = user["id"]
            text = format_user(user)
            is_attended = attended_users[user_id]
            if datetime.fromisoformat(event["date_and_time"]) > datetime.now():
                await callback.message.answer(text=text, parse_mode="html")
            elif is_attended is None:
                builder = InlineKeyboardBuilder()
                builder.button(text=attended, callback_data=ConfirmationUserEventCallback(event_id=callback_data.event_id, user_id=user["id"], attended=True).pack())
                builder.button(text=not_attended, callback_data=ConfirmationUserEventCallback(event_id=callback_data.event_id, user_id=user["id"], attended=False).pack())
                await callback.message.answer(text=text, reply_markup=builder.as_markup(), parse_mode="html")
            else:
                await callback.message.answer(text=text + f"\n{attended}" if is_attended else text + f"\n{not_attended}", parse_mode="html")

    except Exception as e:
        await callback.answer("⚠️ Ошибка при получении пользователей!\nОбратитесь к @sancheser")
        logging.error(msg=e)


@events_router.callback_query(ConfirmationUserEventCallback.filter())
async def event_register(callback: types.CallbackQuery, callback_data: ConfirmationUserEventCallback):
    resp = await user_is_attended(
        telegram_id=callback.from_user.id,
        event_id=callback_data.event_id,
        user_id=callback_data.user_id,
        attented=callback_data.attended,
    )
    if resp.status_code == httpx.codes.NO_CONTENT:
        await callback.message.delete()
    await callback.answer("Пользователь отмечен")

# @events_router.message(lambda message: message.text == "➕ Добавить мероприятие")
# async def start_template(message: types.Message):
#     template = (
#         "📌 Название: \n"
#         "📝 Описание: \n"
#         "📅 Дата и время: \n"
#         "💰 Награда: \n"
#         "📍 Место: \n"
#         "🖼️ Фото: (прикрепите)"
#     )
#     await message.answer(f"📋 Скопируйте и заполните:\n\n{template}")
