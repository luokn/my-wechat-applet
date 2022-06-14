from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class TeamCRUD(BaseCRUD[models.Team]):
    def __init__(self, db: Session):
        super(TeamCRUD, self).__init__(models.Team, db)
