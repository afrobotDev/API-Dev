from fastapi import FastAPI

from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)
