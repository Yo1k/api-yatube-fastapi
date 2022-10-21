from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings


async_engine = create_async_engine(
        url=settings.async_sqlalchemy_database_url,
        echo=True,
        future=True
)

AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
