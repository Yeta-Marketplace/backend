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


@router.get("/", response_model=List[models.YardSaleRead])
def read_yardsales(
    db: Session = Depends(deps.get_session),
    location: models.Location = Depends(),
    distance: float = 25,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve yard sales.
    """
    # monitor_location(location)
    yardsales = crud.yardsale.get_multi_near_location(db, location=location, distance=distance, skip=skip, limit=limit)
    return yardsales


@router.post("/", response_model=models.YardSaleRead)
def create_yardsale(
    *,
    db: Session = Depends(deps.get_session),
    yardsale_in: models.YardSaleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new yard sale.
    """
    # if not is_located_in_US(yardsale_in.latitude, yardsale_in.longitude):
    #     raise HTTPException(
    #         status_code=400, detail="Only supports US locations."
    #     )
    yardsale = crud.yardsale.create(db, obj_in=yardsale_in, user_id=current_user.id)
    return yardsale


# @router.post("/open", response_model=models.YardSaleRead)
# def create_yardsale_open(
#     *,
#     db: Session = Depends(deps.get_session),
#     yardsale_in: models.YardSaleCreate,
# ) -> Any:
#     """
#     Create new yard sale.
#     """
#     if not is_located_in_US(yardsale_in.latitude, yardsale_in.longitude):
#         raise HTTPException(
#             status_code=400, detail="Only supports US locations."
#         )
#     yardsale = crud.yardsale.create(db, obj_in=yardsale_in)
#     return yardsale