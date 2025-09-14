from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.endpoints.users import get_current_user, check_roles
from app.database import get_async_session
from app.models import Chat, User
from app.schemas import ChatRead, ChatWrite, ChatUpdate

router = APIRouter(prefix="/chats")

@router.get("/", response_model=list[ChatRead])
async def get_chats(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)

    result = await session.execute(select(Chat))
    chats = result.scalars().all()
    return chats

@router.get("/me", response_model=list[ChatRead])
async def get_chats(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(User)
        .options(selectinload(User.chats))
        .where(User.id == current_user.id)
    )
    user = result.scalars().first()
    return user.chats

@router.get("/{chat_id}", response_model=ChatRead)
async def get_chat_by_id(chat_id: int, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)

    result = await session.execute(select(Chat).where(User.id == chat_id))
    chat_db = result.scalar_one_or_none()

    if chat_db is None:
        raise HTTPException(404, "Chat not found")

    return chat_db

@router.post("/")
async def create_chat(chat: ChatWrite, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    chat_db = Chat(**chat.model_dump())
    chat_db.user_id = current_user.id
    session.add(chat_db)
    await session.commit()
    await session.refresh(chat_db)
    return ChatRead(**chat_db.to_dict())

@router.put("/{chat_id}")
async def update_chat(chat_id: int, chat: ChatUpdate, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Chat).where(Chat.id == chat_id))
    chat_db = result.scalar_one_or_none()

    if chat_db is None:
        raise HTTPException(404, "Chat not found")
    
    chat_data = chat.model_dump(exclude_none=True)

    for key, value in chat_data.items():
        setattr(chat_db, key, value)
    
    session.add(chat_db)
    await session.commit()
    await session.refresh(chat_db)
    return ChatRead(**chat_db.to_dict())

@router.delete("/{chat_id}")
async def delete_chat(chat_id: int, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Chat).where(Chat.id == chat_id))
    chat_db = result.scalar_one_or_none()

    if chat_db is None:
        raise HTTPException(404, "Chat not found")
    
    await session.delete(chat_db)
    await session.commit()
    return {"detail": "Succesful delete chat!"}
