from fastapi import APIRouter

from src.schemas.token import TokenEmailData
from src.schemas.reservation import ReservationEmailData
from src.helpers.messages import send_notification
from src.helpers.messages import (
    VERIFICATION_TOKEN_BODY,
    VERIFICATION_TOKEN_SUBJECT,
    RESET_TOKEN_BODY,
    RESET_TOKEN_SUBJECT,
    RESERVATION_SUBJECT,
    RESERVATION_BODY,
    build_message,
)


router = APIRouter()


@router.post(
    "/verification-token",
    summary="Send token to email",
    description="Using SMTP send verification token to email",
    response_description="Token sent",
)
async def send_verification_token(data: TokenEmailData):
    msg = build_message(
        VERIFICATION_TOKEN_SUBJECT,
        VERIFICATION_TOKEN_BODY.format(token=data.token),
    )
    await send_notification(msg, data.email)
    return data


@router.post(
    "/reset-token",
    summary="Send token to email",
    description="Using SMTP send reset password token to email",
    response_description="Token sent",
)
async def send_token(data: TokenEmailData):
    msg = build_message(
        RESET_TOKEN_SUBJECT,
        RESET_TOKEN_BODY.format(token=data.token),
    )
    await send_notification(msg, data.email)
    return data


@router.post(
    "/reservation",
    summary="Send ",
    description="Using SMTP send notification about reservation",
    response_description="Token sent",
)
async def send_notification_about_reseservation(data: ReservationEmailData):
    msg = build_message(
        RESERVATION_SUBJECT,
        RESERVATION_BODY.format(
            date=data.date, time_start=data.time_start, time_end=data.time_end
        ),
    )
    await send_notification(msg, data.email)
    return data
