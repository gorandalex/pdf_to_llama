import enum
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, aliased
from .users import User
from docubot.database.models import Document, Tag

from typing import Optional, Type

from .tags import get_or_create_tags
from ..database.models.vectorstore import VectorStore


async def get_all_vectorstores(db: Session, current_user: User):
    sq = select(VectorStore).filter_by(user_id=current_user.id)
    sq_res = db.execute(sq)
    return sq_res.scalars().all()


async def get_vectorstore_by_name(name: str, db: Session, current_user: User):
    sq = select(VectorStore).filter_by(name=name)
    sq_res = db.execute(sq)
    vectorstore = sq_res.scalar_one_or_none()
    if vectorstore.user_id != current_user.id:
        return None
    return vectorstore
