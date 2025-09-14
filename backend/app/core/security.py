import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, timezone, datetime
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config import get_secret_key


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="api/users/token", auto_error=False)

SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(username=email)
    except InvalidTokenError as e:
        print(e)
        raise credentials_exception

def check_roles(role: str):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not admin rules.")
