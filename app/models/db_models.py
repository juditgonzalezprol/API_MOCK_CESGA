"""SQLAlchemy database models."""
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base


class JobStatus(str, PyEnum):
    """Job status enumeration following Slurm naming."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Job(Base):
    """Job model representing a batch compute job."""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)
    
    # User-provided data
    fasta_sequence = Column(Text, nullable=False)
    fasta_filename = Column(String, nullable=False)
    
    # Hardware requirements
    gpus = Column(Integer, default=0)
    cpus = Column(Integer, default=1)
    memory_gb = Column(Float, default=4.0)
    max_runtime_seconds = Column(Integer, default=3600)
    
    # Job state
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, index=True)
    
    # Timing
    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Result data (JSON-serializable paths or inline)
    output_pdb_path = Column(String, nullable=True)
    output_cif_path = Column(String, nullable=True)
    confidence_json_path = Column(String, nullable=True)
    logs_path = Column(String, nullable=True)
    biological_data_path = Column(String, nullable=True)
    accounting_data_path = Column(String, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Job(id={self.id}, status={self.status})>"
