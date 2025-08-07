from __future__ import annotations

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .datasources.mssql import MssqlConnector
from .datasources.postgres import PostgresConnector
from .exceptions import MissingDSNError
from .factories import ConnectorFactory


def _ensure_dsn(dsn: str | None, name: str) -> str:
    if not dsn:
        raise MissingDSNError(f"{name} is required")
    return dsn


class Container(containers.DeclarativeContainer):
    """Dependency-injector container wiring connectors."""

    config = providers.Configuration()

    postgres_engine = providers.Singleton(
        create_async_engine,
        providers.Callable(_ensure_dsn, config.POSTGRES_DSN, "POSTGRES_DSN"),
        echo=False,
    )

    mssql_engine = providers.Singleton(
        create_async_engine,
        providers.Callable(_ensure_dsn, config.MSSQL_DSN, "MSSQL_DSN"),
        echo=False,
    )

    postgres_session = providers.Singleton(
        sessionmaker,
        postgres_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    mssql_session = providers.Singleton(
        sessionmaker,
        mssql_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    postgres_connector = providers.Factory(PostgresConnector, postgres_session)
    mssql_connector = providers.Factory(MssqlConnector, mssql_session)

    connector_factory = providers.Factory(
        ConnectorFactory,
        backends={
            "postgres": postgres_connector.provider,
            "mssql": mssql_connector.provider,
        },
    )

