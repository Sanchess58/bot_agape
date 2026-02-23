from datetime import datetime
from typing import Any

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from users.services import user_info
from .callbacks import GetUserEventCallback, RegisterEventCallback


async def builder_buttons_by_event(
    builder: InlineKeyboardBuilder,
    event_id: int,
    telegram_id: int,
    button_text: str,
) -> list[InlineKeyboardBuilder]:
    builder.button(
        text=button_text,
        callback_data=RegisterEventCallback(event_id=event_id).pack()
    )
    user = await user_info(telegram_id)
    if user["is_admin"]:
        builder.button(
            text="Участники",
            callback_data=GetUserEventCallback(event_id=event_id).pack()
        )


def format_event(event: dict) -> str:
    dt = datetime.fromisoformat(event["date_and_time"])
    return (
        f"📌 <b>{event['name']}</b>\n\n"
        f"📝 {event['description']}\n\n"
        f"📍 {event['location']}\n\n"
        f"📅 {dt.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"💰 Награда: {event['reward']} монет\n\n"
    )


async def generate_event_message(builder: InlineKeyboardBuilder, event: dict, message: types.Message) -> types.Message:
    if not event["photo_url"]:
        return await message.answer(
            text=format_event(event),
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    return await message.answer_photo(
        photo=event["photo_url"],
        caption=format_event(event),
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


def parse_event_text(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    event = {}
    for line in lines:
        if line.startswith("📌 Название:"):
            event["name"] = line.replace("📌 Название:", "").strip()
        elif line.startswith("📝 Описание:"):
            event["description"] = line.replace("📝 Описание:", "").strip()
        elif line.startswith("📅 Дата и время:"):
            event["date_and_time"] = line.replace("📅 Дата и время:", "").strip()
        elif line.startswith("💰 Награда:"):
            event["reward"] = line.replace("💰 Награда:", "").strip()
        elif line.startswith("📍 Место:"):
            event["location"] = line.replace("📍 Место:", "").strip()
        
    return event
