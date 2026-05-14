from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "first post", "content": "it is first post", "id": 1},
    {"title": "second post", "content": "it is the second", "id": 2},
]


@app.get("/posts")
def get_data():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    print(post.model_dump())
    return {"data": post.model_dump()}
