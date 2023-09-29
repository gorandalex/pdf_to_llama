from typing import List, Optional, Any

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from docubot.database.connect import get_db
from docubot.database.models import UserRole, User
from docubot.schemas.document_comments import CommentBase, CommentPublic, CommentUpdate
from docubot.repository import comments as repository_comments
from docubot.repository import documents as repository_documents
from docubot.utils.filters import UserRoleFilter
from docubot.services.auth import get_current_active_user

router = APIRouter(prefix='/documents/comments', tags=["Document comments"])


@router.post("/", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(
        body: CommentBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    The create_comment function creates a new comment in the database.

    :param body: CommentBase: Get the body of the comment
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user who is currently logged in
    :return: A comment object
    """
    document = await repository_documents.get_document_by_id(body.document_id, db)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    return await repository_comments.create_comment(
        current_user.id, body.document_id, body.data.strip(), db
    )


@router.get(
    '/',
    response_model=List[CommentPublic],
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def get_comments_by_document_or_user_id(
        document_id: Optional[int] = None,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    if user_id is None and document_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Both user_id or document_id must be provided")

    return await repository_comments.get_comments_by_document_or_user_id(
        user_id, document_id, skip, limit, db
    )


@router.get("/{comment_id}", response_model=CommentPublic)
async def get_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    comment = await repository_comments.get_comment_by_id(comment_id, db)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return comment


@router.put("/", response_model=CommentPublic)
async def update_comment(
        body: CommentUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    comment = await repository_comments.update_comment(body.comment_id, body.data, db)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DocumentComment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Comment update is allowed only for user that create comment")

    return comment


@router.delete('/{comment_id}', dependencies=[Depends(UserRoleFilter(UserRole.moderator))])
async def remove_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    comment = await repository_comments.remove_comment(comment_id, db)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return comment
