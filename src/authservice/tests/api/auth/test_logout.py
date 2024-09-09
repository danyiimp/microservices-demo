from httpx import AsyncClient
import pytest

from tests.helpers import get_bearer_header


@pytest.mark.usefixtures("setup_db")
class TestLogout:
    async def test_logout(self, ac: AsyncClient, logged_in_user_data):
        token = logged_in_user_data["token"]
        response = await ac.post(
            "/auth/jwt/logout", headers=get_bearer_header(token)
        )
        assert response.status_code == 204

    async def test_logout_unauthorized(self, ac: AsyncClient):
        response = await ac.post("/auth/jwt/logout")
        assert response.status_code == 401
