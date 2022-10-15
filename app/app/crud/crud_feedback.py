
from .base import CRUDBase
from sqlmodel import Session

from app.models import Feedback, FeedbackCreate, FeedbackUpdate

class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):
    def create(self, db: Session, *, obj_in: FeedbackCreate, user_id: int) -> Feedback:
        new_feedback: Feedback = self.model.from_orm(obj_in)
        new_feedback.user_id = user_id
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback

feedback = CRUDFeedback(Feedback)