"""Background job scheduler - state machine execution."""
import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.db_models import JobStatus, Job
from app.services.job_service import JobService

logger = logging.getLogger(__name__)


class JobScheduler:
    """Scheduler for managing job state transitions."""
    
    def __init__(self):
        """Initialize scheduler with DB connection."""
        # Create sync engine for background tasks
        self.engine = create_engine(
            settings.database_url,
            echo=False,  # Logging configuration controls verbosity
            connect_args={"check_same_thread": False},
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.job_service = JobService()
    
    async def start(self):
        """Start the background scheduler loop."""
        logger.info("Starting job scheduler...")
        while True:
            try:
                await self.process_pending_jobs()
                await asyncio.sleep(1)  # Check every second
            except Exception as e:
                logger.error(f"Error in job scheduler: {e}")
                await asyncio.sleep(2)
    
    async def process_pending_jobs(self):
        """Process jobs that need state transitions."""
        db = self.SessionLocal()
        try:
            # Find PENDING jobs that should become RUNNING
            now = datetime.utcnow()
            pending_jobs = db.query(Job).filter(Job.status == JobStatus.PENDING).all()
            
            for job in pending_jobs:
                elapsed = (now - job.created_at).total_seconds()
                
                # Transition to RUNNING after configured delay
                if elapsed >= settings.pending_to_running_delay:
                    logger.info(f"Transitioning job {job.id} to RUNNING")
                    self.job_service.Mark_job_running(db, job.id)
            
            # Find RUNNING jobs that should become COMPLETED
            running_jobs = db.query(Job).filter(Job.status == JobStatus.RUNNING).all()
            
            for job in running_jobs:
                elapsed = (now - job.started_at).total_seconds() if job.started_at else 0
                
                # Transition to COMPLETED after configured delay
                if elapsed >= settings.running_to_completed_delay:
                    logger.info(f"Transitioning job {job.id} to COMPLETED")
                    self.job_service.mark_job_completed(db, job.id)
        
        except Exception as e:
            logger.error(f"Error processing jobs: {e}")
            db.rollback()
        finally:
            db.close()


async def start_scheduler():
    """Factory function to start the scheduler."""
    scheduler = JobScheduler()
    await scheduler.start()
