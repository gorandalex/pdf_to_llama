from pydantic import BaseModel
from pydantic.schema import datetime


# class VectorstoreModel(BaseModel):
#     name: str


class VectorstoreResponse(BaseModel):
    id: int = 1
    name: str
    url: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
