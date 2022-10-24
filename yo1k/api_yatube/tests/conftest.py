import asyncio
from typing import TypeAlias, TYPE_CHECKING

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    AsyncEngine
from sqlalchemy.orm import sessionmaker

from yo1k.api_yatube.models import Base
from yo1k.api_yatube.tests.utils import SQLiteDBTest


if TYPE_CHECKING:
    TSession: TypeAlias = sessionmaker[AsyncSession]
else:
    # anything that doesn't raise an exception
    TSession: TypeAlias = AsyncSession

test_engine: AsyncEngine = create_async_engine(
        url="sqlite+aiosqlite:///:memory:",
        future=True
)
TestSession: TSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> SQLiteDBTest:
    db = SQLiteDBTest(
            engine=test_engine,
            base=Base
    )
    await db.create_tables()
    yield db
    await db.drop_tables()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_tables(db):
    yield db
    await db.delete_tables()


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    session = TestSession()
    try:
        yield session
    finally:
        await session.close()

pytest_plugins = [
    'yo1k.api_yatube.tests.fixtures.fixture_users',
]
