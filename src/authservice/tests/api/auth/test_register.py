import pytest

from httpx import AsyncClient


@pytest.mark.usefixtures("setup_db")
class TestRegister:
    async def test_register(self, user_data, ac: AsyncClient):
        response = await ac.post("/auth/register", json=user_data)
        assert response.status_code == 201

    async def test_register_invalid_email(self, user_data, ac: AsyncClient):
        user_data["email"] = "invalid_email"
        response = await ac.post("/auth/register", json=user_data)
        assert response.status_code == 422

    async def test_register_existing_user(
        self, registered_user_data, ac: AsyncClient
    ):
        response = await ac.post("/auth/register", json=registered_user_data)
        assert response.status_code == 400
