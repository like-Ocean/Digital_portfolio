from pydantic import BaseModel, Field


class CreateProjectModel(BaseModel):
    user_id: int = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(None)


class ChangeProjectModel(BaseModel):
    project_id: int = Field(...)
    name: str = Field(None)
    description: str = Field(None)


class DeleteProjectModel(BaseModel):
    user_id: int = Field(...)


class DeleteFileModel(BaseModel):
    file_id: str = Field(...)
    project_id: int = Field(...)
