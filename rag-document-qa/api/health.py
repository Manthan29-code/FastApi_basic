# GET /api/v1/health
from fastapi import APIRouter


routes = APIRouter()

@routes.get("/helth")
def health():
    return {{"health" : "good"}}