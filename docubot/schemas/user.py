import enum

from datetime import datetime
from strenum import StrEnum
from typing import Optional, List

from pydantic import EmailStr, constr

from docubot.database.models import UserRole, UserLevel
from docubot.schemas.documents import DocumentPublic
from .core import DateTimeModelMixin, IDModelMixin, CoreModel


class UserBase(CoreModel):
    """
    Leaving off password and salt from base model
    """
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    level: UserLevel = "bronze"
    email_verified: bool


class UserInfo(CoreModel):
    """
    Leaving off password and salt from base model
    """
    username: str
    first_name: str
    last_name: str


    class Config:
        orm_mode = True


class UserPublic(DateTimeModelMixin, UserBase, IDModelMixin):
    class Config:
        orm_mode = True


class UserCreate(CoreModel):
    username: constr(min_length=3, max_length=20, regex="[a-zA-Z0-9_-]+$")
    email: EmailStr
    first_name: constr(min_length=3, max_length=100)
    last_name: constr(min_length=3, max_length=100)
    password: constr(min_length=6, max_length=20)


class UserCreateResponse(CoreModel):
    user: UserPublic
    detail: str = "User successfully created"


class UserPasswordUpdate(CoreModel):
    old_password: constr(min_length=6, max_length=20)
    new_password: constr(min_length=6, max_length=20)


class EmailModel(CoreModel):
    email: EmailStr


class ChangeRoleEnum(StrEnum):
    user = UserRole.user
    moderator = UserRole.moderator


class ChangeRole(CoreModel):
    user_id: int
    role: ChangeRoleEnum


class ChangeLevel(CoreModel):
    user_id: int
    level: str


class UserProfile(IDModelMixin):
    username: str
    first_name: str
    last_name: str
    number_of_documents: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProfileUpdate(CoreModel):
    username: Optional[constr(
        min_length=3, max_length=20, regex="[a-zA-Z0-9_-]+$")] = None
    first_name: Optional[constr(min_length=3, max_length=100)] = None
    last_name: Optional[constr(min_length=3, max_length=100)] = None


class SearchResults(CoreModel):
    users: List[UserInfo]
    documents: List[DocumentPublic]
