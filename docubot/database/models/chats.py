from typing import Optional
from datetime import datetime

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .users import User


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(500), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"))
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE", onupdate="CASCADE"))
    answer: Mapped[str] = mapped_column(String(500), index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    user: Mapped[User] = relationship(backref="chats")
    