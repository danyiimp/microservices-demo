import aiosmtplib

from email.message import EmailMessage

from src.config import settings


TOKEN_EMAIL_SUBJECT = "Authentication Token"
TOKEN_EMAIL_BODY = "Your authentication token is: {token}"


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
