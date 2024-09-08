from typing import Optional, TypeVar
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models, exceptions
from fastapi_users.manager import BaseUserManager
from fastapi_users.db import BaseUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select


class MyUserProtocol(models.UserProtocol[models.ID]):
    username: str


UP = TypeVar("UP", bound=MyUserProtocol)


class MyBaseUserDatabase(BaseUserDatabase[UP, models.ID]):
    async def get_by_username(self, username: str) -> Optional[UP]:
        """Get a single user by username."""
        raise NotImplementedError()


class MySQLAlchemyUserDatabase(
    SQLAlchemyUserDatabase[UP, models.ID], MyBaseUserDatabase[UP, models.ID]
):
    async def get_by_username(self, username: str) -> Optional[UP]:
        stmt = select(self.user_table).where(
            self.user_table.username == username
        )
        return await self._get_user(stmt)


class MyBaseUserManager(BaseUserManager[UP, models.ID]):
    user_db: MyBaseUserDatabase[UP, models.ID]

    async def get_by_username(self, username: str) -> UP:
        """
        Get a user by username.

        :param username: Username of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_username(username)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def get_user(self, credentials: str) -> Optional[UP]:
        """
        Get a user by username or email.

        :param credentials: Username or email of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        try:
            return await self.get_by_username(credentials)
        except exceptions.UserNotExists:
            pass

        try:
            return await self.user_db.get_by_email(credentials)
        except exceptions.UserNotExists:
            pass

        raise exceptions.UserNotExists()

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_user(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = (
            self.password_helper.verify_and_update(
                credentials.password, user.hashed_password
            )
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(
                user, {"hashed_password": updated_password_hash}
            )

        return user
