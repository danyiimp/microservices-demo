import pytest

from httpx import AsyncClient


@pytest.mark.usefixtures("setup_db")
class TestResetPassword:
    async def test_reset_password(
        self, ac: AsyncClient, verified_user_data, mocked_responses
    ):
        response = await ac.post(
            "/auth/forgot-password",
            json={"email": verified_user_data["email"]},
        )
        assert response.status_code == 202

        # Mocked callback response which contains the token
        callback_response = mocked_responses.last_response()
        token = callback_response["token"]

        response = await ac.post(
            "/auth/reset-password",
            json={
                "token": token,
                "password": "new_password",
            },
        )
        assert response.status_code == 200

        # Login with the new password
        response = await ac.post(
            "/auth/jwt/login",
            data={
                "username": verified_user_data["username"],
                "password": "new_password",
            },
        )
        assert response.status_code == 200
