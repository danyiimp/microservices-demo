from fastapi import APIRouter

from src.schemas.token import TokenEmailData
from src.helpers.messages import send_notification
from src.helpers.messages import (
    TOKEN_EMAIL_BODY,
    TOKEN_EMAIL_SUBJECT,
    build_message,
)


router = APIRouter()


@router.post(
    "/token",
    summary="Send token to email",
    description="Using SMTP send authentication token to email",
    response_description="Token sent",
)
async def send_token(data: TokenEmailData):
    msg = build_message(
        TOKEN_EMAIL_SUBJECT, TOKEN_EMAIL_BODY.format(token=data.token)
    )
    await send_notification(msg, data.email)
    return data
