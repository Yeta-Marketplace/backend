
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, DateTime
from datetime import datetime


if TYPE_CHECKING:
    from .user import User

class FeedbackBase(SQLModel):
    description: str


class Feedback(FeedbackBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_on: datetime = Field(default_factory=datetime.utcnow)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="feedbacks")


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackRead(FeedbackBase):
    id: int


class FeedbackUpdate(SQLModel):
    description: Optional[str]
