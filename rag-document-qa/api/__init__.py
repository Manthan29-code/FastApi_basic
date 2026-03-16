from .health import routes as healthRoute
from fastapi import APIRoute

router = APIRouter()
router.include_router(healthRoute)