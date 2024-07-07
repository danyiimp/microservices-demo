from sqlalchemy.orm import mapped_column, Mapped
from fastapi_users.db import SQLAlchemyBaseUserTable

from .database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
