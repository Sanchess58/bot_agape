from datetime import datetime
from typing import Any

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import base64_to_file
from events.requests import get_event, users_at_event
from users.services import user_info
from .callbacks import GetUserEventCallback, RegisterEventCallback


async def builder_info_register_button(
    builder: InlineKeyboardBuilder,
    event_id: int,
    button_text: str,
) -> None:
    builder.button(
        text=button_text,
        callback_data=RegisterEventCallback(event_id=event_id).pack()
    )


async def builder_button_event_users(
    builder: InlineKeyboardBuilder,
    event_id: int,
    telegram_id: str,
) -> None:
    user = await user_info(telegram_id)
    if not user["is_admin"]:
        return
    users_in_event = await users_at_event(telegram_id, event_id)
    builder.button(
        text=f"Участники ({len(users_in_event)})",
        callback_data=GetUserEventCallback(event_id=event_id).pack()
    )


def format_event(event: dict) -> str:
    dt = datetime.fromisoformat(event["date_and_time"])
    return (
        f"📌 <b>{event['name']}</b>\n\n"
        f"📝 {event['description']}\n\n"
        f"📍 {event['location']}\n\n"
        f"📅 {dt.strftime('%d.%m.%Y %H:%M') if dt.hour != 0 else dt.strftime('%d.%m.%Y')}\n\n"  # TODO: Временный костыль
        f"💰 Награда: {event['reward']} монет\n\n"
    )


async def generate_event_message(builder: InlineKeyboardBuilder, event: dict, message: types.Message) -> types.Message:
    event = await get_event(event_id=event["id"], telegram_id=message.from_user.id)
    if not event["photo_url"]:
        return await message.answer(
            text=format_event(event),
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )

    photo_file = await base64_to_file(event)

    return await message.answer_photo(
        photo=photo_file,
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
