import httpx
from typing import Optional

from constants import API_BASE_URL


class APIClient:
    def __init__(self) -> None:
        self._token: Optional[str] = None

    async def _login(self, telegram_id: int) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{API_BASE_URL}/users/login",
                json={"telegram_id": telegram_id}
            )
            resp.raise_for_status()
            data = resp.json()
            self._token = data["token"]

    async def request(self, method: str, url: str, telegram_id: int, **kwargs) -> httpx.Response:
        """
        Делаем запрос с токеном. Если 401 — пытаемся заново логиниться и повторяем.
        """
        headers = kwargs.pop("headers", {})
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        async with httpx.AsyncClient() as client:
            resp = await client.request(method, f"{API_BASE_URL}{url}", headers=headers, **kwargs)

            if resp.status_code == httpx.codes.UNAUTHORIZED:
                await self._login(telegram_id)
                headers["Authorization"] = f"Bearer {self._token}"
                resp = await client.request(method, f"{API_BASE_URL}{url}", headers=headers, **kwargs)
            if resp.status_code in [httpx.codes.INTERNAL_SERVER_ERROR, httpx.codes.BAD_GATEWAY]:
                resp.raise_for_status()
            return resp

    # async def request_form_data(d):
    #     async with httpx.AsyncClient() as client:
    #         # Получаем файл фото
    #         file_info = await bot.get_file(photo_id)
    #         file_path = file_info.file_path
    #         file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    #         # Скачиваем фото
    #         async with session.get(file_url) as resp:
    #             photo_bytes = await resp.read()

    #         # Отправляем multipart/form-data
    #         form = aiohttp.FormData()
    #         form.add_field('name', data['name'])
    #         form.add_field('description', data['description'])
    #         form.add_field('date_and_time', data['date_and_time'])
    #         form.add_field('reward', str(data['reward']))
    #         form.add_field('location', data['location'])
    #         form.add_field('photo', photo_bytes, filename='photo.jpg', content_type='image/jpeg')

    #         async with session.post(url, data=form) as response:
    #             if response.status == 200:
    #                 print("✅ Успешно отправлено")
    #             else:
    #                 print("❌ Ошибка:", await response.text())

api_client = APIClient()
