from httpx import AsyncClient
import pytest

from tests.helpers import get_bearer_header


@pytest.mark.usefixtures("setup_db")
class TestMe:
    async def test_me_get(self, ac: AsyncClient, logged_in_user_data):
        token = logged_in_user_data["token"]
        response = await ac.get("/users/me", headers=get_bearer_header(token))
        assert response.status_code == 200
        assert response.json()["username"] == logged_in_user_data["username"]
        assert response.json()["email"] == logged_in_user_data["email"]

    async def test_me_get_unauthorized(self, ac: AsyncClient):
        response = await ac.get("/users/me")
        assert response.status_code == 401

    async def test_me_patch(self, ac: AsyncClient, logged_in_user_data):
        token = logged_in_user_data["token"]
        response = await ac.patch(
            "/users/me",
            headers=get_bearer_header(token),
            json={"email": "new_user@example.com"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "new_user@example.com"

    async def test_me_patch_unauthorized(self, ac: AsyncClient):
        response = await ac.patch(
            "/users/me", json={"password": "new_password"}
        )
        assert response.status_code == 401
