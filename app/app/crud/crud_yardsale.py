from typing import List

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

        37   - LAT
        -122 - LONG

        SELECT *
        FROM (
            SELECT 
                id,
                (
                    3959 *
                    ACOS(
                        COS(RADIANS( LAT )) * 
                        COS(RADIANS(latitude)) * 
                        COS(
                            RADIANS(longitude) - 
                            RADIANS( LONG )
                        ) + 
                        SIN(RADIANS( LAT )) * 
                        SIN(RADIANS(latitude))
                    )
                ) AS distance
            FROM "yardsale"
        ) as ys
        WHERE distance < 100
        ORDER BY distance LIMIT 20 OFFSET 0;
        """
        sin = sqlalchemy.func.SIN
        cos = sqlalchemy.func.COS
        acos = sqlalchemy.func.ACOS
        radians = sqlalchemy.func.RADIANS

        statement = select(YardSale).where(
            3959 * acos(
                cos(radians(location.latitude)) * 
                cos(radians(YardSale.latitude)) * 
                cos(
                    radians(YardSale.longitude) - 
                    radians(location.longitude)
                ) +
                sin(radians(location.latitude)) *
                sin(radians(YardSale.latitude))
            ) < distance
        ).offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()

yardsale = CRUDYardSale(YardSale)