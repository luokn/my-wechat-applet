from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Comment(Base):
    msg = Column(String(512), nullable=False)
    time = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    competition_id = Column(Integer, ForeignKey("competition.id"), nullable=False)
    #
    user = relationship("User", uselist=False)
    competition = relationship("Competition", uselist=False)
    replies = relationship("Reply", back_populates="comment", cascade="all, delete", passive_deletes=True)
