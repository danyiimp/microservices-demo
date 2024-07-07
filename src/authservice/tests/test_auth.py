from pydantic import BaseModel
from httpx import AsyncClient


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class TestAuthService:
    verify_token: str
    access_token: str
    reset_token: str

    @classmethod
    def get_bearer_header(cls):
        return {"Authorization": f"Bearer {cls.access_token}"}

    @classmethod
    async def login(cls, ac: AsyncClient, username: str, password: str):
        response = await ac.post("/auth/jwt/login", data={
            "username": username,
            "password": password
        })
        assert response.status_code == 200
        return response

    @staticmethod
    async def test_register(ac: AsyncClient):
        response = await ac.post("/auth/register", json={
            "username": "string",
            "email": "user@example.com",
            "password": "string",
        })

        assert response.status_code == 201

    @classmethod
    async def test_request_verify_login(cls, ac: AsyncClient, capfd):
        response = await ac.post("/auth/request-verify-token", json={
            "email": "user@example.com"
        })

        assert response.status_code == 202

        out, err = capfd.readouterr()
        cls.verify_token = out.split()[-1]

    @classmethod
    async def test_verify(cls, ac: AsyncClient):
        response = await ac.post("/auth/verify", json={
            "token": cls.verify_token
        })

        assert response.status_code == 200

    @classmethod
    async def test_login_by_username(cls, ac: AsyncClient):
        await cls.login(ac, "string", "string")

    @classmethod
    async def test_login_by_email(cls, ac: AsyncClient):
        response = await cls.login(ac, "user@example.com", "string")
        response_model = LoginResponse(**response.json())
        cls.access_token = response_model.access_token

    @classmethod
    async def test_logout(cls, ac: AsyncClient):
        response = await ac.post("/auth/jwt/logout", headers=cls.get_bearer_header())

        assert response.status_code == 204

    @classmethod
    async def test_forgot_password(cls, ac: AsyncClient, capfd):
        response = await ac.post("/auth/forgot-password", json={
            "email": "user@example.com"
        })

        assert response.status_code == 202

        out, err = capfd.readouterr()
        cls.reset_token = out.split()[-1]

    @classmethod
    async def test_reset_password_and_login(cls, ac: AsyncClient):
        response = await ac.post("/auth/reset-password", json={
            "token": cls.reset_token,
            "password": "new_string"
        })

        assert response.status_code == 200

        await cls.login(ac, "string", "new_string")
