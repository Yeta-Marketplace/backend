from .base import CRUDBase
from sqlmodel import Session

from app.models import YardSale, YardSaleCreate, YardSaleUpdate

class CRUDYardSale(CRUDBase[YardSale, YardSaleCreate, YardSaleUpdate]):
    def create(self, db: Session, *, obj_in: YardSaleCreate, user_id=None) -> YardSale:
        new_yardsale: YardSale = self.model.from_orm(obj_in)
        if user_id:
            new_yardsale.user_id = user_id
        db.add(new_yardsale)
        db.commit()
        db.refresh(new_yardsale)
        return new_yardsale

yardsale = CRUDYardSale(YardSale)