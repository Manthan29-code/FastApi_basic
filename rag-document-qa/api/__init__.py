from .health import routes as healthRoute
from .collections import router as collectionsRoute
from .documents import router as documentsRoute
from .query import router as queryRoute
from fastapi import APIRouter

router = APIRouter()
router.include_router(healthRoute)
router.include_router(collectionsRoute)
router.include_router(documentsRoute)
router.include_router(queryRoute)