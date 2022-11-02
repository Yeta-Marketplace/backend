
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.product import Product
# from app.schemas.product import ProductCreate, ProductUpdate

# product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)

from .crud_user import user
from .crud_yardsale import yardsale
from .crud_feedback import feedback
from .crud_event_type import event_type