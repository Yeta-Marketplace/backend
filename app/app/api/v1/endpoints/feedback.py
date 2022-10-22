from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=models.FeedbackRead)
def submit_feedback(
    *,
    db: Session = Depends(deps.get_session),
    feedback_in: models.FeedbackCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit feedback/bug report.
    """
    feedback = crud.feedback.create(db, obj_in=feedback_in, user_id=current_user.id)
    return feedback
