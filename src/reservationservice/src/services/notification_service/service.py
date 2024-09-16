import aiohttp

from src.services.notification_service.config import NOTIFICATION_URL


async def send_notification(
    email: str, time_start: str, time_end: str, url: str = NOTIFICATION_URL
):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json={
                "email": email,
                "time_start": time_start,
                "time_end": time_end,
            },
        ) as response:
            response.raise_for_status()
