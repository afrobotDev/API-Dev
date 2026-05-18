from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import Post as PostTable
from app.models import PostCreate, PostResponse

router = APIRouter()


@router.get("/posts")
def get_data(db: Session = Depends(get_db)):
    posts = db.scalars(select(PostTable)).all()
    return [PostResponse.model_validate(post).model_dump() for post in posts]


@router.post("/posts", status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostTable(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return PostResponse.model_validate(new_post).model_dump()


@router.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.get(PostTable, id)
    if post is not None:
        return PostResponse.model_validate(post).model_dump()
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")


@router.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.get(PostTable, id)
    if post is not None:
        db.delete(post)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")


@router.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    existing = db.get(PostTable, id)
    if existing is not None:
        for field, value in post.model_dump().items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return PostResponse.model_validate(existing).model_dump()
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")







