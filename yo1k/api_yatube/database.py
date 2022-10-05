from sqlalchemy import create_engine, MetaData, event, DDL
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432"
BASE_SCHEMA_NAME = "yatube"

engine = create_engine(
        url=SQLALCHEMY_DATABASE_URL,
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
