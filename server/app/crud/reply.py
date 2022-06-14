from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class ReplyCRUD(BaseCRUD[models.Reply]):
    def __init__(self, db: Session):
        super(ReplyCRUD, self).__init__(models.Reply, db)
