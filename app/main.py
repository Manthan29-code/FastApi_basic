from fastapi import FastAPI
from app.api import routes
from app.db.session import engine, Base
from app.models import userModel  ## use app/models/__init__.py in can\se of multiple model import 
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "*"  # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes)

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)