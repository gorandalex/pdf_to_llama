from typing import Optional
from datetime import datetime

from sqlalchemy import (
    func,
    String,
    ForeignKey,
    Integer,
    Table,
    Column,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .tags import Tag
from .base import Base
from .users import User
from .chats import Chat



document_m2m_tag = Table(
    "document_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("document_id", Integer, ForeignKey("documents.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1200))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(backref="documents")
    tags: Mapped[Tag] = relationship("Tag", secondary=document_m2m_tag, backref="documents", lazy='joined')
    chats: Mapped[Chat] = relationship(backref="document", cascade="all, delete-orphan")


    