from typing import List, Optional, Any

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from docubot.database.connect import get_db
from docubot.database.models import UserRole, User
from docubot.schemas.chats import ChatBase, ChatPublic
from docubot.repository import chats as repository_chats
from docubot.repository import documents as repository_documents
from docubot.utils.filters import UserRoleFilter
from docubot.services.auth import get_current_active_user

router = APIRouter(prefix='/documents/chats', tags=["Document chats"])


@router.post("/", response_model=ChatPublic, status_code=status.HTTP_201_CREATED)
async def create_chat(
        body: ChatBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    document = await repository_documents.get_document_by_id(body.document_id, db)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found document")

    return await repository_chats.create_chat(
        current_user.id, body.document_id, body.question.strip(), db
    )


@router.get(
    '/',
    response_model=List[ChatPublic],
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def get_chats_by_document_or_user_id(
        document_id: Optional[int] = None,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    if user_id is None and document_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Both user_id or document_id must be provided")

    return await repository_chats.get_chats_by_document_or_user_id(
        user_id, document_id, skip, limit, db
    )


@router.get("/{chat_id}", response_model=ChatPublic)
async def get_chat(
        chat_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    chat = await repository_chats.get_chat_by_id(chat_id, db)

    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found 2")

    return chat



@router.delete('/{chat_id}', dependencies=[Depends(UserRoleFilter(UserRole.moderator))])
async def remove_chat(
        chat_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:

    chat = await repository_chats.remove_chat(chat_id, db)

    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found 1")

    return chat
