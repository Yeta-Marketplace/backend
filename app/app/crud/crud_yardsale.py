from typing import List
from datetime import date

import sqlalchemy
from .base import CRUDBase
from sqlmodel import Session, select

from app.models import YardSale, YardSaleCreate, YardSaleUpdate, Location

class CRUDYardSale(CRUDBase[YardSale, YardSaleCreate, YardSaleUpdate]):
    def create(self, db: Session, *, obj_in: YardSaleCreate, user_id=None) -> YardSale:
        new_yardsale: YardSale = self.model.from_orm(obj_in)
        if user_id:
            new_yardsale.user_id = user_id
        db.add(new_yardsale)
        db.commit()
        db.refresh(new_yardsale)
        return new_yardsale
    
    def get_multi_near_location(
        self, db: Session, *, location: Location, distance: float, skip: int = 0, limit: int = 100
    ) -> List[YardSale]:
        """
        distance in miles
        """
        sin = sqlalchemy.func.SIN
        cos = sqlalchemy.func.COS
        acos = sqlalchemy.func.ACOS
        radians = sqlalchemy.func.RADIANS

        if distance >= 1000:
            # Avoids expensive calculation
            distance_filter = True
        else:
            distance_filter = (3959 * acos(
                cos(radians(location.latitude)) * 
                cos(radians(YardSale.latitude)) * 
                cos(
                    radians(YardSale.longitude) - 
                    radians(location.longitude)
                ) +
                sin(radians(location.latitude)) *
                sin(radians(YardSale.latitude))
            )) < distance

        statement = select(YardSale).where(
            (YardSale.end_date >= date.today()) & distance_filter
        ).order_by(YardSale.end_date).offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()

yardsale = CRUDYardSale(YardSale)