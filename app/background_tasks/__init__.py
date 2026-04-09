"""Package initialization for background tasks."""
from app.background_tasks.job_scheduler import start_scheduler

__all__ = ["start_scheduler"]
