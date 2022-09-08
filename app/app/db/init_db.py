
from sqlmodel import Session
from app.core.config import settings
from app import crud
from app.models import UserCreate

def init_db(db: Session) -> None:
    # TODO: Create Admin User if missing

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.user.create(db, obj_in=user_in)
        user.is_superuser = True
        db.add(user)
        db.commit()
