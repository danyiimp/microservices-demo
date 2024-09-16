from fastapi import FastAPI

from src.api.reservations import router as reservation_router
from src.core.auth import router as auth_router


app = FastAPI(
    title="Reservation Service",
    description="Service for reservation time",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(reservation_router)
