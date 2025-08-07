from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager, Dict, List

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession


class DataSource(ABC):
    """Abstract base class for data source connectors."""

    @abstractmethod
    async def execute_one(self, sql: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Execute a query and return a single row as a dictionary."""

    @abstractmethod
    async def execute_all(self, sql: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        """Execute a query and return all rows as list of dictionaries."""

    @abstractmethod
    async def execute_df(self, sql: str, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        """Execute a query and return the result as a pandas DataFrame."""

    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Return a new async session."""

    @abstractmethod
    def begin_uow(self) -> AsyncContextManager[AsyncSession]:
        """Return async context manager for unit of work."""

