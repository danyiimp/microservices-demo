import pytest

from httpx import AsyncClient

from tests.fixtures.aioresponses import myaioresponses


@pytest.fixture
def user_data():
    return {
        "username": "username",
        "password": "password",
        "email": "user@example.com",
    }


@pytest.fixture
async def registered_user_data(
    ac: AsyncClient, user_data, mocked_responses: myaioresponses
):
    response = await ac.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Mocked callback response which contains the token
    callback_response = mocked_responses.last_response()
    user_data["token"] = callback_response["token"]

    return user_data


@pytest.fixture
async def verified_user_data(ac: AsyncClient, registered_user_data):
    response = await ac.post(
        "/auth/verify",
        json={"token": registered_user_data["token"]},
    )
    assert response.status_code == 200

    return registered_user_data


@pytest.fixture
async def logged_in_user_data(ac: AsyncClient, verified_user_data):
    response = await ac.post(
        "/auth/jwt/login",
        data=verified_user_data,
    )
    assert response.status_code == 200

    access_token = response.json()["access_token"]
    verified_user_data["token"] = access_token

    return verified_user_data
