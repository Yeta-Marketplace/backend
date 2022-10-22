from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core.config import settings

router = APIRouter()


# TODO: Move to utils
def is_located_in_US(latitude, longitude):
    return (25 <= latitude <= 50) and (-120 <= longitude <= -65)


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
    if not is_located_in_US(yardsale_in.latitude, yardsale_in.longitude):
        raise HTTPException(
            status_code=400, detail="Only supports US locations."
        )
    yardsale = crud.yardsale.create(db, obj_in=yardsale_in, user_id=current_user.id)
    return yardsale


@router.post("/open", response_model=models.YardSaleRead)
def create_yardsale(
    *,
    db: Session = Depends(deps.get_session),
    yardsale_in: models.YardSaleCreate,
) -> Any:
    """
    Create new yard sale.
    """
    if not is_located_in_US(yardsale_in.latitude, yardsale_in.longitude):
        raise HTTPException(
            status_code=400, detail="Only supports US locations."
        )
    yardsale = crud.yardsale.create(db, obj_in=yardsale_in)
    return yardsale