import pandas as pd
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from connector_engine.datasources.postgres import PostgresConnector
from connector_engine.datasources.mssql import MssqlConnector


@pytest.mark.asyncio
async def test_postgres_execute_one():
    session = AsyncMock()
    result = MagicMock()
    result.mappings.return_value.first.return_value = {"v": 1}
    session.execute.return_value = result

    connector = PostgresConnector(lambda: session)
    row = await connector.execute_one("SELECT 1")

    assert row == {"v": 1}
    session.execute.assert_called()
    session.commit.assert_called()
    session.close.assert_called()


@pytest.mark.asyncio
async def test_mssql_execute_all_rollback():
    session = AsyncMock()
    session.execute.side_effect = RuntimeError("boom")
    connector = MssqlConnector(lambda: session)

    with pytest.raises(RuntimeError):
        await connector.execute_all("SELECT 1")

    session.rollback.assert_called()
    session.close.assert_called()


@pytest.mark.asyncio
async def test_execute_df_closes_session():
    session = AsyncMock()
    session.bind.sync_engine = MagicMock()
    connector = PostgresConnector(lambda: session)
    df = pd.DataFrame({"a": [1]})
    with patch("pandas.read_sql_query", return_value=df) as read_sql:
        res = await connector.execute_df("SELECT 1")
    assert res.equals(df)
    read_sql.assert_called()
    session.close.assert_called()
