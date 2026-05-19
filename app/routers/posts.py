from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import Post as PostTable
from app.db_models import User as UserTable
from app.models import PostCreate, PostResponse
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/")
def get_data(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100, description="Number of posts to return"),
    offset: int = Query(default=0, ge=0, description="Number of posts to skip"),
    search: str | None = Query(default=None, description="Search in title and content"),
):
    query = select(PostTable)
    if search:
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pattern = f"%{escaped}%"
        query = query.where(
            PostTable.title.ilike(pattern, escape="\\")
            | PostTable.content.ilike(pattern, escape="\\")
        )
    query = query.offset(offset).limit(limit)
    posts = db.scalars(query).all()
    return [PostResponse.model_validate(post).model_dump() for post in posts]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    new_post = PostTable(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return PostResponse.model_validate(new_post).model_dump()


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.get(PostTable, id)
    if post is not None:
        return PostResponse.model_validate(post).model_dump()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    post = db.get(PostTable, id)
    if post is not None:
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
        db.delete(post)
        db.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.put("/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    existing = db.get(PostTable, id)
    if existing is not None:
        if existing.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
        for field, value in post.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return PostResponse.model_validate(existing).model_dump()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")







