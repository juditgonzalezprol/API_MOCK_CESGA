"""Package initialization for routers."""
from app.routers.jobs import router as jobs_router
from app.routers.proteins import router as proteins_router

__all__ = ["jobs_router", "proteins_router"]
