from api_client import APIClient


async def user_info(telegram_id: int):
    resp = await APIClient().request(
        "GET",
        f"/users/{telegram_id}",
        telegram_id=telegram_id,
    )
    return resp.json()


async def get_users(telegram_id: int, ids: list[int] | None = None):
    resp = await APIClient().request(
        "GET",
        "/users/",
        telegram_id=telegram_id,
        params={"ids": ids} if ids else None
    )
    return resp.json()
