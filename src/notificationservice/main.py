from fastapi import FastAPI

from src.routers import router


app = FastAPI(
    title="Notification Service",
    description="Service for sending notifications",
    version="0.1.0",
)
app.include_router(router)
