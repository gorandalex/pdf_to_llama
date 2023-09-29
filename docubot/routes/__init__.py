from fastapi import APIRouter

from . import auth
from . import users
from . import documents
from . import document_comments
from . import tags
from . import openai_chat


router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(documents.router)
router.include_router(document_comments.router)
router.include_router(tags.router)
router.include_router(openai_chat.router)

__all__ = (
    'router',
)
