from fastapi import FastAPI, HTTPException
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

@app.post("/posts", status_code=201)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"data": post}
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
