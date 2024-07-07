from fastapi_users import schemas
from pydantic import BaseModel


class UserUsername(BaseModel):
    username: str


class UserRead(schemas.BaseUser[int], UserUsername):
    pass


class UserCreate(schemas.BaseUserCreate, UserUsername):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
