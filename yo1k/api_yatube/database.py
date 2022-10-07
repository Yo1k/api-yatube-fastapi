from sqlalchemy import create_engine, MetaData, event, DDL
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings


BASE_SCHEMA_NAME = settings.base_schema_name


engine = create_engine(
        url=settings.sqlalchemy_database_url,
        echo=True,
        future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(schema=BASE_SCHEMA_NAME)
Base = declarative_base(metadata=metadata_obj)

event.listen(
        Base.metadata,
        "before_create",
        DDL(f"CREATE SCHEMA IF NOT EXISTS {BASE_SCHEMA_NAME}"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
