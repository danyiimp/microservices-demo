import aiohttp


async def send_token(url: str, token: str, email: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json={
                "token": token,
                "email": email,
            },
        ) as response:
            response.raise_for_status()
