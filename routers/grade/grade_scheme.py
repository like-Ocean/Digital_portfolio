from pydantic import BaseModel, Field


class AddGradeModel(BaseModel):
    user_id: int = Field(...)
    project_id: int = Field(...)
    grade: float = Field(...)
