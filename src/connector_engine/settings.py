from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings for database connections."""

    POSTGRES_DSN: str = Field(..., description="PostgreSQL DSN")
    MSSQL_DSN: str = Field(..., description="MSSQL DSN")

    class Config:
        env_file = ".env"

