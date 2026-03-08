from fastapi import APIRouter
from .health import routers as health_router
from .summarize import router as summarize_router

router = APIRouter()
router.include_router(health_router)
router.include_router(summarize_router, prefix="/v1")