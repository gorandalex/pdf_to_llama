from fastapi import APIRouter

from . import auth
from . import users
from . import documents
from . import chats
from . import tags
from . import openai_chat
from . import users_tokens
from . import vectorstore


router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(documents.router)
router.include_router(chats.router)
router.include_router(tags.router)
router.include_router(openai_chat.router)
router.include_router(users_tokens.router)
router.include_router(vectorstore.router)

__all__ = (
    'router',
)
