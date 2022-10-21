import pytest
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

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.execute(
                    text(
                            f'ATTACH DATABASE \':memory:\' AS '
                            f'{settings.base_schema_name};'
                    )
            )
            await conn.run_sync(self.base.metadata.create_all)

    async def drop_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)


@pytest.fixture(scope="session")
def db():
    db = DBTest(
            engine=test_engine,
            base=Base
    )
    yield db


@pytest.fixture
def db_session():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
