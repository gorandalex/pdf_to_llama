from pydantic import constr

from .core import CoreModel, DateTimeModelMixin, IDModelMixin


class CreateChatRequest(CoreModel):
    question: constr(min_length=5, max_length=500)


class CreateChatResult(CoreModel):
    question: constr(min_length=5, max_length=500)


class ChatPublic(DateTimeModelMixin, CreateChatResult, IDModelMixin):
    user_id: int
    answer: constr(min_length=5, max_length=500)

    class Config:
        orm_mode = True
