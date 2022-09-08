from typing import Optional

from sqlmodel import Session, select

from app.models import User, UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.exec(select(User).where(User.email == email)).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # TODO: Change this to use UserCreate
        new_user = obj_in.dict()
        new_user['hashed_password'] = get_password_hash(obj_in.password)
        del new_user['password']
        new_user = User.parse_obj(new_user)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate):
        update_data = obj_in.dict(exclude_unset=True)
        if update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
