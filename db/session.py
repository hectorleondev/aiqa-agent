# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import get_settings
from typing import Generator
from contextlib import contextmanager

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.is_development  # Log SQL in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.

    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database session (use in workers)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
