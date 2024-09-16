import jwt
import aiohttp

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from src.core.config import settings


router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


@router.post("/auth")
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.AUTH_URL,
            data={
                "username": form_data.username,
                "password": form_data.password,
            },
            headers=headers,
        ) as response:
            response.raise_for_status()
            result = await response.json()
            return Token(**result)


class Token(BaseModel):
    access_token: str
    token_type: str


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, [settings.ALGORITHM])
        user_id: str = payload.get("sub")
    except InvalidTokenError:
        raise credentials_exception
    return user_id
