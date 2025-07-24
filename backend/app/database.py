"""Database configuration and session management.

This module configures SQLAlchemy for use with a local SQLite database.  For
other database engines (PostgreSQL, MySQL, etc.) you can modify the
`DATABASE_URL` accordingly.  The session generator can be used as a
dependency in FastAPI path functions to provide a transactional scope for
database operations.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./flightdata.db"

# Create the SQLAlchemy engine.  The `connect_args` option is specific to
# SQLite and required when using SQLite in a multi‑threaded environment such as
# Uvicorn.  For other databases this argument can be removed.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class.  Each instance of SessionLocal will be
# tied to a database connection and transaction.  Use a separate session per
# request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models.  All ORM classes should inherit from this.
Base = declarative_base()

def get_db():
    """Yield a SQLAlchemy session for dependency injection in FastAPI.

    This generator ensures that the session is closed after the request is
    completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()