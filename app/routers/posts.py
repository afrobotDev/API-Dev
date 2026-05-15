from fastapi import APIRouter, HTTPException

from app.database import my_posts
from app.models import Post

router = APIRouter()


@router.get("/posts")
def get_data():
    return {"data": my_posts}


@router.post("/posts", status_code=201)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = max((p["id"] for p in my_posts), default=0) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@router.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"data": post}
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")


@router.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")


@router.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = id
    for i, existing in enumerate(my_posts):
        if existing["id"] == id:
            my_posts[i] = post_dict
            return {"data": post_dict}
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
