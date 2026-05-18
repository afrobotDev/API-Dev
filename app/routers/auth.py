from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db_models import User as UserTable
from app.database import get_db
from app.models import UserResponse, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def auth_user(user_info: UserLogin, db: Session = Depends(get_db)):
    user = db.scalars(select(UserTable).where(UserTable.email == user_info.email)).first()
    if not user or not pwd_context.verify(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    return UserResponse.model_validate(user).model_dump()


