from typing import Any

from api_client import APIClient


async def get_products(telegram_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        "GET",
        "/products",
        telegram_id=telegram_id,
    )
    return resp.json()
