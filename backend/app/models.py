from datetime import datetime
from sqlalchemy import ForeignKey, func, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, DeclarativeBase, relationship, mapped_column


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

    chats: Mapped[list["Chat"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="New Chat")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="chats")

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    data: Mapped[str]
    from_user: Mapped[str]

    chat: Mapped["Chat"] = relationship(back_populates="messages")
