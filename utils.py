import base64
from aiogram.types import BufferedInputFile


def get_name_weekday(week_day: int) -> str:
    return ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"][week_day]


async def base64_to_file(obj: dict) -> BufferedInputFile:
    photo_bytes = base64.b64decode(obj["photo_url"])

    return BufferedInputFile(
        file=photo_bytes,
        filename="photo.jpg" 
    )
