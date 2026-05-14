from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def get_data():
    return {"message": "welcome to fastapi"}

@app.post("/posts")
def create_post(post: Post):
    print(post.dict())
    return {"data": post}
