import aiosmtplib

from email.message import EmailMessage

from src.config import settings


VERIFICATION_TOKEN_SUBJECT = "Verification Token"
VERIFICATION_TOKEN_BODY = "Your verification token is: {token}"

RESET_TOKEN_SUBJECT = "Password reset Token"
RESET_TOKEN_BODY = "Your password reset token is: {token}"


def build_message(subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.EMAIL
    message.set_content(body)
    return message


async def send_notification(message: str, recipient: str):
    message["To"] = recipient
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.LOGIN,
        password=settings.PASSWORD,
    )
