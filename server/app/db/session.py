from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core import settings

engine = create_engine(settings.DATABASE, pool_pre_ping=True)
#
SessionLocal = sessionmaker(bind=engine)
