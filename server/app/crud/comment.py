from typing import List
from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class CommentCRUD(BaseCRUD[models.Comment]):
    def __init__(self, db: Session):
        super(CommentCRUD, self).__init__(models.Comment, db)

    def query_multi(self, skip: int = 0, limit: int = 100) -> List[models.Comment]:
        return self.db.query(models.Comment).order_by(models.Comment.time.desc()).offset(skip).limit(limit).all()
