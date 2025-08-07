import asyncio

from connector_engine.containers import Container
from connector_engine.settings import Settings


async def main() -> None:
    container = Container()
    container.config.from_pydantic(Settings())
    factory = container.connector_factory()

    pg = factory.get("postgres")
    row = await pg.execute_one(
        "SELECT :value AS value", {"value": 1}
    )
    rows = await pg.execute_all(
        "SELECT * FROM some_table WHERE id > :id", {"id": 10}
    )
    df = await pg.execute_df(
        "SELECT * FROM some_table WHERE flag = :flag", {"flag": True}
    )

    ms = factory.get("mssql")
    row_ms = await ms.execute_one(
        "SELECT TOP (1) :value AS value", {"value": 2}
    )
    rows_ms = await ms.execute_all(
        "SELECT * FROM other_table WHERE id > :id", {"id": 20}
    )
    df_ms = await ms.execute_df(
        "SELECT * FROM other_table WHERE flag = :flag", {"flag": False}
    )

    print(row, rows, df)
    print(row_ms, rows_ms, df_ms)


if __name__ == "__main__":
    asyncio.run(main())
