from pydantic import BaseModel, Field
from fastapi import Form


class AddCertificateModel(BaseModel):
    user_id: int = Field(default=Form(...))
    name: str = Field(default=Form(...), min_length=1)
    company: str | None = Field(default=Form(None))
    link: str | None = Field(default=Form(None))


class EditCertificateModel(BaseModel):
    certificate_id: int = Field(default=Form(...))
    name: str = Field(default=Form(), min_length=1)
    company: str | None = Field(default=Form(None))
    link: str | None = Field(default=Form(None))


class DeleteCertificateModel(BaseModel):
    certificate_id: int = Field(...)
    file_id: str = Field(...)
