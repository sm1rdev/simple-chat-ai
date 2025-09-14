import asyncio
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette import EventSourceResponse
from openai import OpenAI

from app.config import get_open_ai_api_key
from app.database import get_async_session
from app.models import Message

router = APIRouter(prefix="/events/openai")

client = OpenAI(api_key=get_open_ai_api_key())

start_prompt = """На вход подаётся история переписки в формате:
    - User: сообщение  
    - You: ответ
    Нужно:
    Проанализировать всю переписку.
    Ответить только на последнее сообщение пользователя.
    На выходе писать только текст ответа Элины, без пометок You:.
    Стиль Элины — добрая, чуткая, поддерживающая девушка, которая помогает морально, отвечает мягко и с заботой.
    """


async def generate_events(message: str):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": start_prompt + message}],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield {"event": "message", "data": delta.content}
        await asyncio.sleep(0.1)

@router.get("/")
async def send_open_ai_response(chat_id: int = Query(...), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    messages_db = result.scalars().all()

    prompt = ""
    for message_db in messages_db:
        if message_db.from_user == "me":
            prompt += f"User:\n{message_db.data}\n"
        else:
            prompt += f"You:\n{message_db.data}\n"
        
    return EventSourceResponse(generate_events(prompt))
