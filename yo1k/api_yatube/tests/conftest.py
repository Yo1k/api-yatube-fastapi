import asyncio
import sys

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from yo1k.api_yatube.models import Base
from yo1k.api_yatube.settings import settings

test_engine = create_async_engine(
        url="sqlite+aiosqlite:///:memory:",
        future=True
)
TestSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
)


class DBTest:
    def __init__(
            self,
            engine=test_engine,
            base=Base
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


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db():
    db = DBTest(
            engine=test_engine,
            base=Base
    )
    await db.create_tables()
    yield db
    await db.drop_tables()


@pytest_asyncio.fixture
async def db_session():
    session = TestSession()
    try:
        yield session
    finally:
        await session.close()
