from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Callable

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import DataSource

logger = logging.getLogger(__name__)


class MssqlConnector(DataSource):
    """MSSQL data source connector."""

    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def execute_one(self, sql: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        logger.debug("Executing one: %s %s", sql, params)
        async with self.begin_uow() as session:
            result = await session.execute(text(sql), params or {})
            row = result.mappings().first()
            return dict(row) if row else {}

    async def execute_all(self, sql: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        logger.debug("Executing all: %s %s", sql, params)
        async with self.begin_uow() as session:
            result = await session.execute(text(sql), params or {})
            rows = result.mappings().all()
            return [dict(r) for r in rows]

    async def execute_df(self, sql: str, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        logger.debug("Executing df: %s %s", sql, params)
        session = self.get_session()
        try:
            df = pd.read_sql_query(sql, session.bind.sync_engine, params=params)
            return df
        finally:
            await session.close()

    async def execute_write(self, sql: str, params: Dict[str, Any] | None = None) -> int:
        logger.debug("Executing write: %s %s", sql, params)
        async with self.begin_uow() as session:
            result = await session.execute(text(sql), params or {})
            return result.rowcount

    async def call_procedure(self, name: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        logger.debug("Calling procedure: %s %s", name, params)
        params = params or {}
        assignments = ", ".join(f"@{k} = :{k}" for k in params)
        sql = f"EXEC {name} {assignments}" if assignments else f"EXEC {name}"
        async with self.begin_uow() as session:
            result = await session.execute(text(sql), params)
            rows = result.mappings().all()
            return [dict(r) for r in rows]

    def get_session(self) -> AsyncSession:
        return self._session_factory()

    def begin_uow(self):  # type: ignore[override]
        @asynccontextmanager
        async def _uow():
            session = self.get_session()
            try:
                logger.debug("Transaction begin")
                yield session
                await session.commit()
                logger.debug("Transaction commit")
            except Exception:
                logger.debug("Transaction rollback")
                await session.rollback()
                raise
            finally:
                await session.close()
                logger.debug("Session closed")

        return _uow()

