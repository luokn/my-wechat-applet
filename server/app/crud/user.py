from typing import Optional

from sqlalchemy.orm import Session

from .. import models
from .base import BaseCRUD


class UserCRUD(BaseCRUD[models.User]):
    def __init__(self, db: Session):
        super(UserCRUD, self).__init__(models.User, db)

    def query_by_openid(self, openid: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.openid == openid).first()
