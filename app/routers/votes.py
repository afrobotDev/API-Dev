from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import Post as PostTable
from app.db_models import User as UserTable
from app.db_models import Vote as VoteTable
from app.models import Vote as VoteSchema
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_for(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    post = db.get(PostTable, vote.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found",
        )

    existing_vote = db.scalars(
        select(VoteTable).where(
            VoteTable.post_id == vote.post_id,
            VoteTable.user_id == current_user.id,
        )
    ).first()

    if vote.vote_dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post",
            )
        new_vote = VoteTable(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote recorded successfully"}

    if not existing_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vote found to remove",
        )
    db.delete(existing_vote)
    db.commit()
    return {"message": "Vote removed successfully"}
