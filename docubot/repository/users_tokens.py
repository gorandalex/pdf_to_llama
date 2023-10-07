from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from docubot.database.models.users_tokens import UserToken
from docubot.schemas.users_tokens import UserTokensModel




async def get_total_user_tokens(user_id, db: Session):
    """
    The get_total_user_tokens function returns the total number of tokens a user has.
    If the user does not exist in the database, it will create an entry for them with 0 tokens.

    :param user_id: Get the user_id from the database
    :param db: Session: Access the database
    :return: A usertoken object
    """

    total_user_tokens = db.query(UserToken).filter(UserToken.user_id == user_id).all()
    if len(total_user_tokens) == 0:
        user_tokens = UserToken(user_id=user_id, total_user_tokens=0, started_at=datetime.now())
        db.add(user_tokens)
        db.commit()
        db.refresh(user_tokens)
    return db.query(UserToken).filter(UserToken.user_id== user_id).first().total_user_tokens


async def add_user_tokens(user_id, user_tokens, db: Session):
    """
    The add_user_tokens function adds user tokens to the database.
    Args:
        user_id (int): The id of the user who is receiving tokens.
        user_tokens (int): The amount of tokens that are being added to the users total token count.
    Returns:
        UserToken: A UserToken object containing all information about a specific users token count and when they were last updated.

    :param user_id: Identify the user in the database
    :param user_tokens: Add the amount of tokens to the user
    :param db: Session: Access the database
    :return: A usertoken object
    """

    total_user_tokens = db.query(UserToken).filter(UserToken.user_id == user_id).all()

    if len(total_user_tokens) == 0:
        total_user_tokens = UserToken(user_id=user_id, total_user_tokens=user_tokens, started_at=datetime.now())
        db.add(total_user_tokens)
        db.commit()
        db.refresh(total_user_tokens)

    if datetime.now() - total_user_tokens[0].started_at > timedelta(hours=24):
        total_user_tokens[0].total_user_tokens = user_tokens
        total_user_tokens[0].started_at = datetime.now()

    else:
        if total_user_tokens[0].total_user_tokens == 0:
            total_user_tokens[0].started_at = datetime.now()
        total_user_tokens[0].total_user_tokens += user_tokens

    db.commit()
    return db.query(UserToken).filter(UserToken.user_id==user_id).first()

