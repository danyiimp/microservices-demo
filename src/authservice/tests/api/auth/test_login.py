import pytest

from httpx import AsyncClient


@pytest.mark.usefixtures("setup_db")
class TestLogin:
    async def test_login_by_username(self, verified_user_data, ac: AsyncClient):
        response = await ac.post(
            "/auth/jwt/login",
            data=verified_user_data,
        )
        assert response.status_code == 200

    async def test_login_by_email(self, verified_user_data, ac: AsyncClient):
        verified_user_data["username"] = verified_user_data["email"]
        response = await ac.post(
            "/auth/jwt/login",
            data=verified_user_data,
        )
        assert response.status_code == 200

    async def test_login_unverified_user(
        self, registered_user_data, ac: AsyncClient
    ):
        response = await ac.post("/auth/jwt/login", data=registered_user_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "LOGIN_USER_NOT_VERIFIED"}

    async def test_login_incorrect_password(
        self, registered_user_data, ac: AsyncClient
    ):
        registered_user_data["password"] = "incorrect_password"
        response = await ac.post("/auth/jwt/login", data=registered_user_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "LOGIN_BAD_CREDENTIALS"}

    async def test_login_incorrect_username(self, user_data, ac: AsyncClient):
        user_data["username"] = "incorrect_username"
        response = await ac.post(
            "/auth/jwt/login",
            data=user_data,
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "LOGIN_BAD_CREDENTIALS"}
