from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from . import schemas, service, models


fastapi_users = FastAPIUsers[models.User, int](
    service.get_user_manager,
    [service.auth_backend],
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])

users_router = APIRouter(prefix="/users", tags=["users"])

auth_router.include_router(
    fastapi_users.get_auth_router(
        service.auth_backend, requires_verification=True
    ),
    prefix="/jwt",
)

auth_router.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate)
)

auth_router.include_router(fastapi_users.get_verify_router(schemas.UserRead))

auth_router.include_router(fastapi_users.get_reset_password_router())

users_router.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate)
)
