from fastapi import FastAPI
from src.routers import auth_router, users_router


app = FastAPI(title="Auth Service", version="0.1.0")
app.include_router(auth_router)
app.include_router(users_router)
