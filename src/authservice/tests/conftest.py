import asyncio
import pytest

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from main import app


pytest_plugins = [
    "tests.fixtures.aioresponses",
    "tests.fixtures.auth",
    "tests.fixtures.db",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
