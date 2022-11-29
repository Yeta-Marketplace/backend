
from typing import TYPE_CHECKING, Optional
from app.custom_types import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


if TYPE_CHECKING:
    from .event import YardSale
    from .feedback import Feedback

class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    full_name: Optional[str]
    is_active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: Optional[str] = Field(default=None, index=True)
    hashed_password: str
    is_superuser: bool = False

    created_on: datetime = Field(default_factory=datetime.utcnow)

    yard_sales: list["YardSale"] = Relationship(back_populates="user")
    feedbacks: list["Feedback"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    full_name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
