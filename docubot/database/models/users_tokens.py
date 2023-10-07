from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .users import User

class UserToken(Base):
    __tablename__ = 'users_tokens'
    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(backref="users_tokens")
    total_user_tokens = Column(Integer, default=0)
    started_at = Column(DateTime, default=func.now(), onupdate=func.now())

