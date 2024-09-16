from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from src.schemas.reservation import ReservationRead, ReservationCreate
from src.services.crud import (
    get_all_reservations,
    create_reservation,
    get_awailable_by_date,
)
from src.services.notification_service.service import send_notification
from src.core.database import get_async_session
from src.core.auth import get_current_user_id

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    dependencies=[Depends(get_current_user_id)],
)


@router.get("/{date}", response_model=list[ReservationRead])
async def awailable_by_date(
    db: Annotated[AsyncSession, Depends(get_async_session)], date: date
):
    res = await get_awailable_by_date(db, date)
    return res


@router.get("/", response_model=list[ReservationRead])
async def all_reservations(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    res = await get_all_reservations(db)
    return res


@router.post("/")
async def create_new_reservation(
    reservation: ReservationCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    result = await create_reservation(db, reservation, user_id)
    await send_notification(user_id, result.start_time, result.end_time)
    return result
