from typing import Optional

from sqlalchemy import update, select
from sqlalchemy.orm import Session
from docubot.database.models.chats import Chat


async def create_chat(user_id: int, document_id: int, question: str, db: Session) -> Chat:

    chat = Chat(
            user_id=user_id,
            document_id=document_id,
            question=question,


        )
    db.add(chat)

    db.commit()
    db.refresh(chat)

    return chat


async def get_chats_by_document_or_user_id(user_id: int, document_id: int, skip: int, limit: int,
                                           db: Session) -> list[Chat]:

    query = select(Chat)

    if document_id:
        query = query.filter(Chat.document_id == document_id)
    if user_id:
        query = query.filter(Chat.user_id == user_id)

    chats = db.scalars(query.offset(skip).limit(limit))

    return chats.all()  # noqa


async def get_chat_by_id(chat_id: int, db: Session) -> Optional[Chat]:

    return db.scalar(
        select(Chat)
        .filter(Chat.id == chat_id)
    )


async def remove_chat(chat_id: int, db: Session) -> Optional[Chat]:

    chat = await get_chat_by_id(chat_id, db)

    if chat:
        db.delete(chat)
        db.commit()

    return chat
