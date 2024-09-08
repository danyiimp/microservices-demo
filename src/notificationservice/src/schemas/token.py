from pydantic import BaseModel, EmailStr


class TokenEmailData(BaseModel):
    token: str
    email: EmailStr
