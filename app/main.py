"""FastAPI application factory and configuration."""
import logging

# Suppress verbose SQLAlchemy logging BEFORE importing any SQLAlchemy modules
sqlalchemy_loggers = [
    "sqlalchemy.engine",
    "sqlalchemy.pool", 
    "sqlalchemy.dialects",
    "sqlalchemy.engine.Engine"
]
for _logger_name in sqlalchemy_loggers:
    logging.getLogger(_logger_name).setLevel(logging.WARNING)

# Now import everything else
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.routers import jobs_router, proteins_router
from app.background_tasks import start_scheduler

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)


# Background task management
scheduler_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle events.
    - Startup: Start the background job scheduler task
    - Shutdown: Cancel the scheduler task
    """
    global scheduler_task
    
    # Startup
    logger.info("Starting CESGA API Simulator...")
    logger.info(f"Database: {settings.database_url}")
    logger.info(f"Job state transitions:")
    logger.info(f"  PENDING -> RUNNING: {settings.pending_to_running_delay}s")
    logger.info(f"  RUNNING -> COMPLETED: {settings.running_to_completed_delay}s")
    
    # Start background scheduler
    scheduler_task = asyncio.create_task(start_scheduler())
    
    yield
    
    # Shutdown
    logger.info("Shutting down CESGA API Simulator...")
    if scheduler_task:
        scheduler_task.cancel()
        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass


# Create FastAPI application
app = FastAPI(
    redirect_slashes=False,
    title=settings.api_title,
    version=settings.api_version,
    description="Mock simulator for CESGA Finis Terrae III supercomputer (Slurm-like interface)",
    lifespan=lifespan,
    # Swagger UI customization - Dark mode theme
    swagger_ui_parameters={
        "displayOperationId": True,
        "deepLinking": True,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        # Dark theme colors
        "colors": {
            "primary": "#00897b",      # Teal
            "secondary": "#1f1f1f",    # Muy oscuro
        },
        # Custom CSS for dark mode styling
        "customCss": """
            :root {
                --bg-color: #1a1a1a;
                --text-color: #e0e0e0;
            }
            * {
                background-color: #1a1a1a !important;
                color: #e0e0e0 !important;
            }
            .topbar { background-color: #0d0d0d !important; }
            .topbar h1, .topbar div { color: #00897b !important; }
            .scheme-container { background-color: #262626 !important; }
            .model-container { background-color: #1f1f1f !important; border: 1px solid #333 !important; }
            .model { background-color: #1f1f1f !important; }
            textarea, input[type="text"], input[type="password"] { 
                background-color: #262626 !important; 
                color: #e0e0e0 !important;
                border: 1px solid #404040 !important;
            }
            .operation-filter-input { background-color: #262626 !important; border: 1px solid #404040 !important; }
            button { background-color: #00897b !important; color: white !important; }
            .btn { background-color: #00897b !important; }
            .try-out { background-color: #1f1f1f !important; }
            .response-col_description__inner { color: #e0e0e0 !important; }
            pre, code { 
                background-color: #0d0d0d !important; 
                color: #00ff00 !important;
                border: 1px solid #333 !important;
            }
            .section { border: 1px solid #333 !important; }
            a { color: #00897b !important; }
            a:visited { color: #009688 !important; }
        """
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Include routers
app.include_router(jobs_router)
app.include_router(proteins_router)

# Serve CIF structure files from PBS_BIEN/
_structures_dir = Path(__file__).parent.parent / "PBS_BIEN"
if _structures_dir.is_dir():
    app.mount("/structures", StaticFiles(directory=str(_structures_dir)), name="structures")
    logger.info(f"Serving CIF structures from {_structures_dir}")


# API metadata endpoints
@app.get(
    "/",
    summary="API root",
    tags=["info"],
)
def root():
    """Root endpoint providing API information."""
    return {
        "title": settings.api_title,
        "version": settings.api_version,
        "description": "CESGA supercomputer simulator for hackathon use",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
        "endpoints": {
            "submit_job": "POST /jobs/submit",
            "get_status": "GET /jobs/{job_id}/status",
            "get_outputs": "GET /jobs/{job_id}/outputs",
            "get_accounting": "GET /jobs/{job_id}/accounting",
            "list_jobs": "GET /jobs/",
        },
    }


@app.get("/health", tags=["info"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version,
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected exceptions globally."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
