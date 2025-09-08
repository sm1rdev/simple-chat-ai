from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import users


origins = [
    "http://localhost:5173"
]

app = FastAPI()

app.include_router(router=users.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
