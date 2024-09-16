from datetime import date

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reservation import Reservation
from src.schemas.reservation import ReservationCreate
from src.schemas.time_interval import TimeInterval
from src.services.db_operations import is_time_intersect, get_busy_time_by_date
from src.helpers.utils import get_awailable_time_intervals


async def create_reservation(
    db: AsyncSession, reservation: ReservationCreate, user_id: int
):
    if await is_time_intersect(db, reservation):
        raise ValueError("Time is intersected with another reservation")
    stmt = insert(Reservation).values(
        user_id=user_id, **reservation.model_dump()
    )
    await db.execute(stmt)
    await db.commit()
    return reservation


async def get_all_reservations(db: AsyncSession):
    stmt = select(Reservation)
    res = await db.scalars(stmt)
    return res.all()


async def get_awailable_by_date(db: AsyncSession, date: date):
    result = await get_busy_time_by_date(db, date)
    busy_time = [TimeInterval(**item) for item in result]
    return get_awailable_time_intervals(date, busy_time)
