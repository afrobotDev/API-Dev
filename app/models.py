from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
