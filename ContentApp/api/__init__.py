from fastapi import APIRouter
from .health import routers as health_router
from .summarize import router as summarize_router
from .sentiment import router as sentiment_router
from .classify import router as classify_router
from .keywords import router as keywords_router
from .rewrite import router as rewrite_router

router = APIRouter()
router.include_router(health_router)
router.include_router(summarize_router, prefix="/v1")
router.include_router(sentiment_router, prefix="/v1/analyzer")
router.include_router(classify_router, prefix="/v1/classifier")
router.include_router(keywords_router, prefix="/v1/keywords")
router.include_router(rewrite_router, prefix="/v1/rewrite")