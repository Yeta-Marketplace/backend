from .base import CRUDBase

from app.models import YardSale, YardSaleCreate, YardSaleUpdate

yardsale = CRUDBase[YardSale, YardSaleCreate, YardSaleUpdate](YardSale)