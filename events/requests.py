from typing import Any

from httpx import Response
from api_client import APIClient


async def events(telegram_id: int, date_from: str, date_to: str) -> dict[str, Any]:
    resp = await APIClient().request(
        method="GET",
        url="/events/",
        telegram_id=telegram_id,
        params={"date_from": date_from, "date_to": date_to}
    )
    return resp.json()


async def get_event(telegram_id: int, event_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        method="GET",
        url=f"/events/{event_id}/",
        telegram_id=telegram_id,
    )
    return resp.json()


async def my_events(telegram_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        "GET",
        "/events/my",
        telegram_id=telegram_id,
    )
    return resp.json()


async def register_to_event(telegram_id: int, event_id: int) -> Response:
    resp = await APIClient().request(
        method="POST",
        url="/events/register",
        telegram_id=telegram_id,
        json={"event_id": event_id},
    )
    return resp


async def cancel_register_to_event(telegram_id: int, event_id: int) -> Response:
    resp = await APIClient().request(
        method="DELETE",
        url=f"/events/{event_id}/register/cancel",
        telegram_id=telegram_id,
    )
    return resp


async def users_at_event(telegram_id: int, event_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        method="GET",
        url=f"/events/{event_id}/users",
        telegram_id=telegram_id,
    )
    return resp.json()


async def user_is_attended(telegram_id: int, event_id: int, user_id: int, attented: bool) -> Response:
    resp = await APIClient().request(
        method="POST",
        url="/events/confirmation",
        telegram_id=telegram_id,
        json={"event_id": event_id, "user_id": user_id, "attended": attented},
    )
    return resp
