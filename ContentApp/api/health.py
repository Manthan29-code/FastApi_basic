from fastapi import APIRouter
from dotenv import load_dotenv
load_dotenv()
import os
routers = APIRouter()
model = os.getenv("MODEL_NAME")
@routers.get("/health")
def health():
    return {
    "status": "healthy",
    "service": "ai-content-toolkit",
    "status": "ok",
    "model": model  , 
    }

