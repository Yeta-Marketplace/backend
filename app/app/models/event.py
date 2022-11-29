
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime

if TYPE_CHECKING:
    from .user import User
    from .event_type import EventType


class EventBase(SQLModel):
    description: Optional[str]

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    start_date: date
    end_date: date



class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="events")
    
    event_type_id: int = Field(default=1, foreign_key="eventtype.id", nullable=False)
    event_type: "EventType" = Relationship(back_populates="events")

    created_on: datetime = Field(default_factory=datetime.utcnow)


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int


class EventUpdate(SQLModel):
    description: Optional[str]

    start_date: Optional[date]
    end_date: Optional[date]
