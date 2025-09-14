from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, Depends, Cookie, Security
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token, validate_token, check_roles
from app.core.security import oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, credentials_exception
from app.database import get_async_session
from app.models import User
from app.schemas import UserRead, UserWrite, UserUpdate


router = APIRouter(prefix="/users")

async def get_current_user(token: str | None = Security(oauth2_scheme), access_token: str | None = Cookie(default=None), session: AsyncSession = Depends(get_async_session)):
    if token == "undefined":
        token = None
    token = token or access_token
    if not token:
        raise credentials_exception
    
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    token_data = validate_token(token)

    result = await session.execute(select(User).where(User.email == token_data.username))
    user_db = result.scalar_one_or_none()
    if user_db is None:
        raise credentials_exception
    
    return user_db

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user_db = result.scalar_one_or_none()
    if user_db is None or not verify_password(form_data.password, user_db.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user_db.email}
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax"
    )

    return {"msg": "Login successful"}
    

@router.get("/", response_model=list[UserRead])
async def get_users(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)
    
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/me", response_model=UserRead)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)

    result = await session.execute(select(User).where(User.id == user_id))
    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_db

@router.post("/")
async def create_user(user: UserWrite, session: AsyncSession = Depends(get_async_session)):
    user.password = hash_password(user.password)
    user_db = User(**user.model_dump())
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return UserRead(**user_db.to_dict())

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)
    
    result = await session.execute(select(User).where(User.id == user_id))
    user_db = result.scalar_one_or_none()

    if user_db is None:    
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_none=True)

    for key, value in user_data.items():
        setattr(user_db, key, value)

    await session.commit()
    await session.refresh(user_db)
    return UserRead(**user_db.to_dict())

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    check_roles(current_user.role)

    result = await session.execute(select(User).where(User.id == user_id))
    user_db = result.scalar_one_or_none()

    if user_db is None:    
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user_db)
    await session.commit()
    return {"detail": "User deleted"}
