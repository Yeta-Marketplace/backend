
from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    full_name: Optional[str]
    email: str = Field(index=True)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    hashed_password: str
    is_active: bool
    is_superuser: bool


class UserCreate(UserBase):
    password: str
    is_active: bool = True


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    password: str