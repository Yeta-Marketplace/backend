
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .user import User


class YardSaleBase(SQLModel):
    description: Optional[str]

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    start_date: datetime
    end_date: datetime


class YardSale(YardSaleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="yard_sales")


class YardSaleCreate(YardSaleBase):
    pass


class YardSaleRead(YardSaleBase):
    id: int


class YardSaleUpdate(SQLModel):
    description: Optional[str]

    start_date: Optional[datetime]
    end_date: Optional[datetime]
