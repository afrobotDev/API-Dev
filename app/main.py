from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
from app.routers.votes import router as votes_router
app = FastAPI()
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(votes_router)
