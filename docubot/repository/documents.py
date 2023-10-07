
import enum
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, aliased
from docubot.database.models import Document, Tag

from typing import Optional, Type

from .tags import get_or_create_tags


class SortMode(enum.Enum):

    NOT_SORT = 'not_sort'
    RAITING = 'average_rating'
    RAITING_DESC = 'average_rating_desc'
    DATE = 'date_added'
    DATE_DESC = 'date_added_desc'


async def get_document_by_id(document_id: int, db: Session) -> Document:
    """
    The get_document_by_id function returns n document from the database.

    :param document_id: int: Filter the documents by id
    :param db: Session: Pass in the database session to use
    :return: A single document object
    """
    return db.scalar(
        select(Document)
        .filter(Document.id == document_id)
    )
    

async def create_document(user_id: int, description: str, tags: list[str], public_id: str, db: Session) -> Document:
    """
    The create_document function creates a new document in the database.

    :param user_id: int: Specify the user who uploaded the document
    :param description: str: Describe the document
    :param tags: list[str]: Specify that the tags parameter is a list of strings
    :param public_id: str: Store the public id of the document in cloudinary
    :param db: Session: Pass in the database session
    :return: An document object
    """
    document = Document(
        user_id=user_id,
        description=description,
        public_id=public_id
    )

    if tags:
        document.tags = await get_or_create_tags(tags, db)

    db.add(document)

    db.commit()

    db.refresh(document)

    return document


async def update_description(document_id: int, description: str, tags: list[str], db: Session) -> Optional[Document]:

    tags = await get_or_create_tags(tags, db)

    document = await get_document_by_id(document_id, db)
    if document:
        document.description = description
        document.tags = tags
        db.commit()
        db.refresh(document)

    return document


async def delete_document(document: Document, db: Session) -> None:

    db.delete(document)
    db.commit()


async def get_documents(
        skip: int,
        limit: int,
        description: str,
        tags: list[str],
        document_id: int,
        user_id: int,
        sort_by: SortMode,
        db: Session
) -> list[Document]:

    query = select(Document)

    if description:
        query = query.filter(Document.description.like(f'%{description}%'))
    if tags:
        for tag in tags:
            query = query.filter(Document.tags.any(Tag.name.ilike(f'%{tag}%')))

    query = query.filter(Document.user_id == user_id)
    if document_id:
        query = query.filter(Document.id == document_id)

    elif sort_by == SortMode.DATE:
        query = query.order_by(Document.created_at.asc())
    elif sort_by == SortMode.DATE_DESC:
        query = query.order_by(Document.created_at.desc())

    document = db.scalars(query)

    return document.unique().all()  # noqa


async def search_documents(data: str, db: Session) -> list[Type[Document]]:

    documents = db.query(Document).filter(Document.description.ilike(f"%{data}%") |
                                       Document.tags.any(Tag.name.ilike(f"%{data}%"))).all()

    return documents


async def count_documents_by_user_id(user_id: int, db: Session) -> int:

    documents_count = db.query(Document).count()

    return documents_count

