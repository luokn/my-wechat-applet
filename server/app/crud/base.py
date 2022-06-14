from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from .. import models

ModelType = TypeVar("ModelType", bound=models.Base)


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model_type: Type[ModelType], db: Session):
        self.model_type, self.db = model_type, db

    def create(self, **values) -> ModelType:
        model = self.model_type(**values)
        self.db.add(model)
        self.db.commit()
        return model

    def update(self, id: int, **values) -> int:
        count = self.db.query(self.model_type).filter(self.model_type.id == id).update(values)
        self.db.commit()
        return count

    def delete(self, id: int) -> int:
        count = self.db.query(self.model_type).filter(self.model_type.id == id).delete()
        self.db.commit()
        return count

    def query(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model_type).filter(self.model_type.id == id).first()

    def query_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model_type).offset(skip).limit(limit).all()

    def query_multi_by(self, skip: int = 0, limit: int = 100, **kwargs) -> List[ModelType]:
        return self.db.query(self.model_type).filter_by(**kwargs).offset(skip).limit(limit).all()
