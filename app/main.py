from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import db_models  # noqa: F401
from app.database import Base, engine
from app.routers.posts import router as posts_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)
