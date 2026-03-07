from typing import Any

from api_client import APIClient


async def user_info(telegram_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        "GET",
        f"/users/{telegram_id}",
        telegram_id=telegram_id,
    )
    return resp.json()


async def get_users(telegram_id: int, ids: list[int] | None = None) -> dict[str, Any]:
    resp = await APIClient().request(
        "GET",
        "/users/",
        telegram_id=telegram_id,
        params={"ids": ids} if ids else None
    )
    return resp.json()
