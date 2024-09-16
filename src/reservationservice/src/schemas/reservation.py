from datetime import datetime
from pydantic import ConfigDict, PositiveInt

from src.schemas.time_interval import TimeInterval


class ReservationBase(TimeInterval):
    pass


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: PositiveInt
    user_id: PositiveInt
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
