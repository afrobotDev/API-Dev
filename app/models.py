from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    description: str | None = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    @field_validator("password")
    def password_length(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password cannot exceed 72 bytes (bcrypt limit)")
        if len(v) < 6:
            raise ValueError("password must be at least 6 characters")
        return v


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
