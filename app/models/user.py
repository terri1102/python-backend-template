from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(SQLModel):
    email: str
    full_name: str
    password: str = Field(min_length=8, max_length=40)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserUpdate(SQLModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
