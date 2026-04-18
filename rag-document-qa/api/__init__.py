from .health import routes as healthRoute
from .collections import router as collectionsRoute
from fastapi import APIRouter

router = APIRouter()
router.include_router(healthRoute)
router.include_router(collectionsRoute)