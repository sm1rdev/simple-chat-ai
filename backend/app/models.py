from datetime import datetime
from sqlalchemy import func, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def to_dict(self, exclude: list[str] = None) -> dict:
        exclude = set(exclude or [])
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(String(128), unique=True)
    role: Mapped[str] = mapped_column(default="user")
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
