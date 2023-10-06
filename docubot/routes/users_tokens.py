from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session

from docubot.database.models import UserRole, User
from docubot.database.connect import get_db

from docubot.schemas.users_tokens import UserTokensModel, UserTokensResponse 
from docubot.repository import users_tokens as repository_users_tokens

from docubot.utils.filters import UserRoleFilter
from docubot.services.auth import get_current_active_user

router = APIRouter(prefix='/users_tokens', tags=["Users_tokens"])


@router.post("/", response_model=UserTokensResponse)
async def add_or_create_users_tokens(
        users_tokens: int = Body(),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    The add_or_create_users_tokens function adds or creates users_tokens for the current user.
    

    :param users_tokens: int: Get the number of tokens to add or create
    :param db: Session: Get the database session
    :param current_user: User: Get the user id from the database
    :return: A list of objects 
    """

    users_tokens = await repository_users_tokens.add_user_tokens(current_user.id, users_tokens, db)
    return users_tokens


@router.get("/", response_model=UserTokensResponse)
async def get_or_create_users_tokens(
        users_tokens: int = Body(),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    The get_or_create_users_tokens function is used to get the total number of tokens a user has.
    It takes in an integer value for users_tokens, and returns the total number of tokens a user has.

    :param users_tokens: int: Get the users_tokens from the body of the request
    :param db: Session: Get the database connection
    :param current_user: User: Get the current user's id
    :return: users_tokens
    """

    users_tokens = await repository_users_tokens.get_total_user_tokens(current_user.id, db)
    return users_tokens