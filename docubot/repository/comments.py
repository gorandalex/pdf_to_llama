from typing import Optional

from sqlalchemy import update, select
from sqlalchemy.orm import Session
from docubot.database.models.document_comments import DocumentComment


async def create_comment(user_id: int, document_id: int, data: str, db: Session) -> DocumentComment:
    """
    The create_comment function creates a new comment in the database.

    :param user_id: int: Specify the user_id of the comment
    :param document_id: int: Identify the document that the comment is being made on
    :param data: str: Pass the comment data to the function
    :param db: Session: Pass in the database session
    :return: A comment object
    """
    comment = DocumentComment(
            user_id=user_id,
            document_id=document_id,
            data=data
        )
    db.add(comment)

    db.commit()
    db.refresh(comment)

    return comment


async def get_comments_by_document_or_user_id(user_id: int, document_id: int, skip: int, limit: int,
                                           db: Session) -> list[DocumentComment]:

    query = select(DocumentComment)

    if document_id:
        query = query.filter(DocumentComment.document_id == document_id)
    if user_id:
        query = query.filter(DocumentComment.user_id == user_id)

    comments = db.scalars(query.offset(skip).limit(limit))

    return comments.all()  # noqa


async def get_comment_by_id(comment_id: int, db: Session) -> Optional[DocumentComment]:
    """
    The get_comment function returns a comment object from the database.

    :param comment_id: int: Filter the comments by id
    :param db: Session: Pass the database session to the function
    :return: A comment object
    """
    return db.scalar(
        select(DocumentComment)
        .filter(DocumentComment.id == comment_id)
    )


async def update_comment(comment_id: int, data: str, db: Session) -> DocumentComment:
    """
    The update_comment function updates a comment in the database.

    :param comment_id: int: Find the comment in the database
    :param data: str: Update the data of a comment
    :param db: Session: Pass the database session to the function
    :return: A comment object
    """
    comment = db.scalar(
            update(DocumentComment)
            .values(data=data)
            .filter(DocumentComment.id == comment_id)
            .returning(DocumentComment)
        )

    db.commit()

    return comment


async def remove_comment(comment_id: int, db: Session) -> Optional[DocumentComment]:
    """
    The remove_comment function removes a comment from the database.

    :param comment_id: int: Specify the id of the comment to be removed
    :param db: Session: Pass in the database session
    :return: The comment that was removed
    """
    comment = await get_comment_by_id(comment_id, db)

    if comment:
        db.delete(comment)
        db.commit()

    return comment
