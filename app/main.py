from fastapi import FastAPI
from app.api.routes import router
from app.db.session import engine, Base
from app.models import userModel  ## use app/models/__init__.py in can\se of multiple model import 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

app.include_router(router)
Base.metadata.create_all(bind=engine)