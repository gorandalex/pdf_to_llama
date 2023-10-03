from pydantic import BaseModel, Field


class UserTokensModel(BaseModel):
    total_user_tokens: int


class UserTokensResponse(UserTokensModel):
    id: int = 1
    user_id: int = 1
    total_user_tokens: int

    class Config:
        orm_mode = True
