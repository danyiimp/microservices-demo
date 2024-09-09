from typing import Annotated

from fastapi import Depends, Request
from fastapi_users import IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from .database import get_async_session
from .config import settings
from .user_manager import MyBaseUserManager, MySQLAlchemyUserDatabase
from .services.notification.service import send_token
from .services.notification.config import (
    RESET_TOKEN_URL,
    VERIFICATION_TOKEN_URL,
)


auth_backend: AuthenticationBackend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl=settings.TOKEN_URL),
    get_strategy=lambda: JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.JWT_LIFETIME_SECONDS,
    ),
)


class UserManager(IntegerIDMixin, MyBaseUserManager[models.User, int]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    reset_password_token_lifetime_seconds = (
        settings.RESET_PASSWORD_TOKEN_LIFETIME_SECONDS
    )
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET
    verification_token_lifetime_seconds = (
        settings.VERIFICATION_TOKEN_LIFETIME_SECONDS
    )

    async def on_after_register(
        self, user: models.User, request: Request | None = None
    ):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: models.User, token: str, request: Request | None = None
    ):
        await send_token(VERIFICATION_TOKEN_URL, token, user.email)

    async def on_after_forgot_password(
        self, user: models.User, token: str, request: Request | None = None
    ):
        await send_token(RESET_TOKEN_URL, token, user.email)


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    yield MySQLAlchemyUserDatabase(session, models.User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
