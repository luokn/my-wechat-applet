from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import models
from ..core import settings


def test_db():
    try:
        engine = create_engine(settings.DATABASE, echo=True)
        SessionLocal = sessionmaker(engine)
        db: Session = SessionLocal()
        assert db.query(models.User.id).count() > 0
    finally:
        db.close()
