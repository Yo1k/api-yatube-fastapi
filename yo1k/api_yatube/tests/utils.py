from sqlalchemy import text

from yo1k.api_yatube.settings import settings


class SQLiteDBTest:
    """
    Database class for testing with using sqlite DBMS and asynchronous
    interactions
    """
    def __init__(
            self,
            engine,
            base
    ):
        self.engine = engine
        self.base = base

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.execute(
                    text(
                            f'ATTACH DATABASE \':memory:\' AS '
                            f'{settings.base_schema_name};'
                    )
            )
            await conn.run_sync(self.base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)

    # autocommit or rollback
    async def delete_tables(self):
        async with self.engine.begin() as conn:
            for table in reversed(self.base.metadata.sorted_tables):
                await conn.execute(table.delete())
