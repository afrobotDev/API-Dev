from pydantic import BaseModel, ConfigDict, EmailStr
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


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)



