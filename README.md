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

## Sample Queries

```python
# Postgres connector with parameters
row = await pg.execute_one(
    "SELECT * FROM users WHERE id = :user_id",
    {"user_id": 1},
)

rows = await pg.execute_all(
    "SELECT * FROM users WHERE age > :age",
    {"age": 21},
)

df = await pg.execute_df(
    "SELECT * FROM purchases WHERE price >= :price",
    {"price": 100},
)

# MSSQL connector with parameters
ms = factory.get("mssql")
row_ms = await ms.execute_one(
    "SELECT TOP (1) * FROM users WHERE id = :user_id",
    {"user_id": 1},
)

rows_ms = await ms.execute_all(
    "SELECT * FROM users WHERE status = :status",
    {"status": "active"},
)
```

## CRUD & Stored Procedures

```python
# Insert
await pg.execute_write(
    "INSERT INTO users(id, name) VALUES (:id, :name)",
    {"id": 1, "name": "Alice"},
)

# Update
await pg.execute_write(
    "UPDATE users SET name = :name WHERE id = :id",
    {"id": 1, "name": "Bob"},
)

# Delete
await pg.execute_write(
    "DELETE FROM users WHERE id = :id",
    {"id": 1},
)

# Stored procedure
rows = await ms.call_procedure("dbo.refresh_stats", {"arg": 10})
```

## Unit of Work

```python
async with pg.begin_uow() as session:
    await session.execute("SELECT 1")
```

Logging output includes connection acquisition, query execution and transaction lifecycle.

