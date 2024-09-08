import aiohttp
from src.services.notification.config import SEND_TOKEN_URL


async def send_token(token: str, email: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            SEND_TOKEN_URL,
            json={
                "token": token,
                "email": email,
            },
        ) as response:
            response.raise_for_status()
