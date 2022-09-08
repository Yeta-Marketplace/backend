from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)  # TODO: Change to indicate that this needs to be a table model
CreateType = TypeVar("CreateType", bound=SQLModel)
UpdateType = TypeVar("UpdateType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateType, UpdateType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.get(self.model, id)
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()
    
    def create(self, db: Session, *, obj_in: CreateType) -> ModelType:
        db_entry = self.model.from_orm(obj_in)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    
    def update(
        self, db: 
        Session, 
        *, 
        db_obj: ModelType, 
        obj_in: UpdateType
    ) -> ModelType:
        new_data = obj_in.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj
