from pydantic import BaseModel, Field, EmailStr


class RegisterModel(BaseModel):
    login: str = Field(..., min_length=1)
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    country: str = Field(...)
    city: str = Field(...)
    password: str = Field(..., min_length=8)


class DeleteAvatarModel(BaseModel):
    user_id: int = Field(...)


class ChangeModel(BaseModel):
    user_id: int = Field(...)
    login: str | None = Field(None)
    email: EmailStr | None = Field(None)
    first_name: str | None = Field(None)
    surname: str | None = Field(None)
    country: str | None = Field(None)
    city: str | None = Field(None)
    avatar: str | None = Field(None)
    phone: str | None = Field(None)
    about: str | None = Field(None)


class DeleteUserModel(BaseModel):
    user_id: int = Field(...)


class ChangePasswordModel(BaseModel):
    user_id: int = Field(...)
    password: str = Field(min_length=8)


class Authorization(BaseModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)
