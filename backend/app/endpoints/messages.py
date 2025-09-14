from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.endpoints.users import get_current_user, check_roles
from app.models import User, Chat, Message
from app.schemas import MessageRead, MessageWrite, MessageUpdate

router = APIRouter(prefix="/chats/{chat_id}/messages")

@router.get("/", response_model=list[MessageRead])
async def get_messages(chat_id: int, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)
    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    messages = result.scalars().all()
    return messages

@router.get("/{message_id}", response_model=MessageRead)
async def get_message_by_id(chat_id: int, message_id: int, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)

    result = await session.execute(select(Message).where(Message.id == message_id, Message.chat_id == chat_id))
    message_db = result.scalar_one_or_none()

    if message_db is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message_db

@router.post("/")
async def create_message(chat_id: int, message: MessageWrite, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)
    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    message_db = Message(chat_id=chat_id, data=message.data, from_user=message.from_user)
    session.add(message_db)
    await session.commit()
    await session.refresh(message_db)
    return MessageRead(**message_db.to_dict())

@router.put("/{message_id}")
async def update_message(chat_id: int, message_id: int, message: MessageUpdate, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)
    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    result = await session.execute(select(Message).where(Message.chat_id == chat_id, Message.id == message_id))
    message_db = result.scalar_one_or_none()

    if message_db is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message_data = message.model_dump(exclude_none=True)

    for key, value in message_data.items():
        setattr(message_db, key, value)

    session.add(message_db)
    await session.commit()
    await session.refresh(message_db)
    return MessageRead(**message_db.to_dict())

@router.delete("/{message_id}")
async def delete_message(chat_id: int, message_id: int, message: MessageUpdate, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)
    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    result = await session.execute(select(Message).where(Message.chat_id == chat_id, Message.id == message_id))
    message_db = result.scalar_one_or_none()

    if message_db is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    await session.delete(message_db)
    await session.commit()
    return {"detail": "Succesful delete message!"}
