"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database
    database_url: str = "sqlite:///./cesga_simulator.db"
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    api_title: str = "CESGA Supercomputer Simulator"
    api_version: str = "1.0.0"
    
    # Job scheduling (seconds)
    pending_to_running_delay: int = 5
    running_to_completed_delay: int = 5
    
    # Hardware limits
    max_gpus_per_job: int = 4
    max_memory_gb: int = 256
    max_cpus_per_job: int = 64
    
    # CORS settings
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
