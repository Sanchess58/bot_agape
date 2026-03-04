from typing import Any

from httpx import Response

from api_client import APIClient


async def get_products(telegram_id: int) -> dict[str, Any]:
    resp = await APIClient().request(
        "GET",
        "/products",
        telegram_id=telegram_id,
    )
    return resp.json()


async def buy_product_request(telegram_id: int, product_id: int) -> Response:
    resp = await APIClient().request(
        "POST",
        f"/products/buy",
        telegram_id=telegram_id,
        json={"id": product_id, "quantity": 1},
    )
    return resp
