from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    nickname: str
    email: EmailStr

class UserRead(User):
    id: int
    role: str

class UserWrite(User):
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class UserUpdate(User):
    nickname: str | None = None
    email: EmailStr | None = None
    role: str | None = None
