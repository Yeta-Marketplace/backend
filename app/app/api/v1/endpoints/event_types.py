from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[models.EventTypeRead])
def read_event_types(
    db: Session = Depends(deps.get_session),
) -> Any:
    """
    Retrieve event categories.
    """
    event_types = crud.event_type.get_multi(db)
    return event_types