from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User as UserTable
from app.models import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users")


@router.post("/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["password"] = pwd_context.hash(user_data["password"])
    new_user = UserTable(**user_data)
    try:
        db.add(new_user)
        db.commit() 
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="A user with this email already exists"
        )
    return UserResponse.model_validate(new_user).model_dump()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(select(UserTable)).all()
    return [UserResponse.model_validate(user).model_dump() for user in users]


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(UserTable, id)
    if user is not None:
        return UserResponse.model_validate(user).model_dump()
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")
