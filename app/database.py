"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

# SQLAlchemy setup
Base = declarative_base()

# For async operations (production-recommended)
async_engine = create_async_engine(
    settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=False,  # Logging configuration controls verbosity
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# For sync operations (simpler for MVP)
engine = create_engine(
    settings.database_url,
    echo=False,  # Logging configuration controls verbosity
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_async_db():
    """Dependency for async database sessions."""
    async with AsyncSessionLocal() as session:
        yield session


def get_db():
    """Dependency for sync database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
