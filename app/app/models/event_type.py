
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime

if TYPE_CHECKING:
    from .event import Event
    from .user import User


class EventTypeBase(SQLModel):
    name: str
    display_name: str
    is_active: bool = True


class EventType(EventTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    events: list["Event"] = Relationship(back_populates="event_type")


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeRead(EventTypeBase):
    id: int


class EventTypeUpdate(SQLModel):
    name: Optional[str]
    display_name: Optional[str]
    is_active: Optional[bool]
