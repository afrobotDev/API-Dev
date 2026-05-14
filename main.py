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
    post_dict = post.model_dump()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}
