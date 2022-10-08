from pathlib import Path
from typing import Optional, Any

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # SQLAlchemy
    base_schema_name: str = "yatube"

    postgres_server: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    sqlalchemy_database_url: Optional[PostgresDsn] = None

    @validator("sqlalchemy_database_url", pre=True)
    def assemble_db_connection(
            cls, v: Optional[str], values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("postgres_user"),
                password=values.get("postgres_password"),
                host=values.get("postgres_server"),
                path=f"/{values.get('postgres_db') or ''}",
        )

    # Authentication
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    secret_key: str


settings = Settings(
        _env_file=BASE_DIR.joinpath(".env"),
        _env_file_encoding="utf-8",
)

