"""Database configuration and migrations utilities."""

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/app",
)
DB_SCHEMA = os.getenv("DATABASE_SCHEMA", "app_schema")

engine = create_engine(DATABASE_URL, future=True)
metadata = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    """Create tables without migrations (mainly for tests)."""
    Base.metadata.create_all(bind=engine)


def run_migrations() -> None:
    """Apply Alembic migrations so schema changes reach the database."""
    cfg = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))
    command.upgrade(cfg, "head")

