from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class CompetitionCRUD(BaseCRUD[models.Competition]):
    def __init__(self, db: Session):
        super(CompetitionCRUD, self).__init__(models.Competition, db)
