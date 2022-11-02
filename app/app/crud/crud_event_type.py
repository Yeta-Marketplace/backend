
from .base import CRUDBase
from app.models import EventType, EventTypeCreate, EventTypeUpdate


event_type = CRUDBase[EventType, EventTypeCreate, EventTypeUpdate](EventType)