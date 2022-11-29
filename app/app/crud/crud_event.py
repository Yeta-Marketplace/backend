from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

import sqlalchemy
from .base import CRUDBase
from sqlmodel import Session, select

from app.models import Event, EventCreate, EventUpdate, Location

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create(self, db: Session, *, obj_in: EventCreate, user_id=None) -> Event:
        new_event: Event = self.model.from_orm(obj_in)
        if user_id:
            new_event.user_id = user_id
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    
    def get_multi_near_location(
        self, db: Session, *, location: Location, distance: float, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        """
        distance in miles
        """
        sin = sqlalchemy.func.SIN
        cos = sqlalchemy.func.COS
        acos = sqlalchemy.func.ACOS
        radians = sqlalchemy.func.RADIANS

        distance_column = (3959 * acos(
            cos(radians(location.latitude)) * 
            cos(radians(Event.latitude)) * 
            cos(
                radians(Event.longitude) - 
                radians(location.longitude)
            ) +
            sin(radians(location.latitude)) *
            sin(radians(Event.latitude))
        ))

        today = datetime.now(ZoneInfo("America/Los_Angeles")).date()

        if distance >= 1000:
            # Avoids expensive calculation
            distance_filter = True
        else:
            distance_filter = distance_column < distance

        statement = select(Event).add_columns(distance_column.label('distance')).where(
            (Event.end_date >= today) & distance_filter
        ).order_by(distance_column, Event.end_date).offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()

event = CRUDEvent(Event)