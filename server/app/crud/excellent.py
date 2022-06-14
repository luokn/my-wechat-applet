from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class ExcellentCRUD(BaseCRUD[models.Excellent]):
    def __init__(self, db: Session):
        super(ExcellentCRUD, self).__init__(models.Excellent, db)
