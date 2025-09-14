from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import users, chats, messages, ai


origins = [
    "http://localhost:5173"
]

app = FastAPI()

app.include_router(router=users.router, prefix="/api")
app.include_router(router=chats.router, prefix="/api")
app.include_router(router=messages.router, prefix="/api")
app.include_router(router=ai.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
