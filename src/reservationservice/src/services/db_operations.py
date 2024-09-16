from datetime import date, datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reservation import Reservation
from src.schemas.reservation import ReservationCreate
from src.core.config import settings


PT = settings.PAUSE_TIME_BEFORE_AND_AFTER_RESERVATION_IN_MIN


async def is_time_intersect(
    db: AsyncSession, reservation: ReservationCreate
) -> bool:
    stmt = select(Reservation).where(
        (Reservation.time_start <= reservation.time_start)
        & (Reservation.time_end >= reservation.time_end)
    )
    res = await db.scalars(stmt)

    return len(res.all()) > 0


async def get_busy_time_by_date(db: AsyncSession, date: date, pt: int = PT):
    min_time = datetime.combine(date, datetime.min.time()) - timedelta(
        minutes=pt
    )
    max_time = datetime.combine(date, datetime.max.time()) + timedelta(
        minutes=pt
    )
    stmt = (
        select(Reservation)
        .where(
            Reservation.time_start.between(min_time, max_time)
            | Reservation.time_end.between(min_time, max_time)
        )
        .order_by(Reservation.time_start.asc())
    )
    res = await db.scalars(stmt)

    return res.all()
