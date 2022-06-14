from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Reply(Base):
    msg = Column(String(512), nullable=False)
    time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comment.id", ondelete="CASCADE"), nullable=False)
    #
    user = relationship("User", uselist=False)
    comment = relationship("Comment", uselist=False, back_populates="replies")
