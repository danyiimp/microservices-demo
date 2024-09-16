from pydantic import BaseModel, EmailStr


class ReservationEmailData(BaseModel):
    time_start: str
    time_end: str
    date: str
    email: EmailStr
