from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
# from app.utils import send_admin_email_feedback

router = APIRouter()

locations = {(39.95, -74.2)}  # Lat, Long

# TODO: Move to utils
def is_located_in_US(latitude, longitude):
    return (20 <= latitude <= 60) and (-130 <= longitude <= -60)

def monitor_location(location: models.Location):
    global locations
    new_location = (round(location.latitude, 2), round(location.longitude, 2))
    if new_location not in locations:
        # Slows down too much, needs to run in a separate thread:
        # send_admin_email_feedback('', -1, f'New Location!! lat: {new_location[0]}, long: {new_location[1]}')
        print(f'New location!!  lat: {new_location[0]}, long: {new_location[1]}')
        locations.add(new_location)


@router.get("/", response_model=List[models.EventRead])
def read_events(
    db: Session = Depends(deps.get_session),
    location: models.Location = Depends(),
    distance: float = 25,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve events.
    """
    # monitor_location(location)
    events = crud.event.get_multi_near_location(db, location=location, distance=distance, skip=skip, limit=limit)
    return events


@router.post("/", response_model=models.EventRead)
def create_event(
    *,
    db: Session = Depends(deps.get_session),
    event_in: models.EventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new event.
    """
    # if not is_located_in_US(event_in.latitude, event_in.longitude):
    #     raise HTTPException(
    #         status_code=400, detail="Only supports US locations."
    #     )
    event = crud.event.create(db, obj_in=event_in, user_id=current_user.id)
    return event


# @router.post("/open", response_model=models.EventRead)
# def create_event_open(
#     *,
#     db: Session = Depends(deps.get_session),
#     event_in: models.EventCreate,
# ) -> Any:
#     """
#     Create new event.
#     """
#     if not is_located_in_US(event_in.latitude, event_in.longitude):
#         raise HTTPException(
#             status_code=400, detail="Only supports US locations."
#         )
#     event = crud.event.create(db, obj_in=event_in)
#     return event