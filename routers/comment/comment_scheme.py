from pydantic import BaseModel, Field


class SendCommentModel(BaseModel):
    user_id: int = Field(...)
    project_id: int = Field(...)
    comment: str = Field(...)


class DeleteCommentModel(BaseModel):
    user_id: int = Field(...)
    comment_id: int = Field(...)
