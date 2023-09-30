from pydantic import constr

from .core import CoreModel, DateTimeModelMixin, IDModelMixin


class ChatBase(CoreModel):

    chat_id: int
    question: constr(min_length=5, max_length=500)
    answer: constr(min_length=5, max_length=500)



class ChatPublic(DateTimeModelMixin, ChatBase, IDModelMixin):
    user_id: int

    class Config:
        orm_mode = True
        