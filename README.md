# Connector Engine

Async database connector engine for Postgres and MSSQL using SQLAlchemy and dependency-injector.

## Installation

```bash
pip install connector_engine
```

## Settings

Configure DSNs via environment or `.env`:

```
POSTGRES_DSN=postgresql+asyncpg://user:pass@localhost:5432/dbname
MSSQL_DSN=mssql+pyodbc://user:pass@localhost:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server
```

Programmatic override:

```python
from connector_engine.settings import Settings

settings = Settings(POSTGRES_DSN="postgresql+asyncpg://...", MSSQL_DSN="mssql+pyodbc://...")
```

## Container Wiring

```python
from connector_engine.containers import Container
from connector_engine.settings import Settings

container = Container()
container.config.from_pydantic(Settings())
factory = container.connector_factory()
pg = factory.get("postgres")

# Usage
result = await pg.execute_one("SELECT 1", {})
```

## Unit of Work

```python
async with pg.begin_uow() as session:
    await session.execute("SELECT 1")
```

Logging output includes connection acquisition, query execution and transaction lifecycle.

