from collections.abc import MutableSequence

import pytest
import pytest_asyncio

from yo1k.api_yatube import schemas, models
from yo1k.api_yatube.services.auth import AuthService


@pytest.fixture
def user_in() -> schemas.UserCreate:
    return schemas.UserCreate(
            username="Tester",
            password="test_password"
    )


@pytest.fixture
def user_in_2() -> schemas.UserCreate:
    return schemas.UserCreate(
            username="Tester2",
            password="test_password",
            email="test@mail.com",
            first_name="Tester",
            last_name="2",
    )


@pytest.fixture
def user_in_update_all_attrs() -> schemas.UserUpdate:
    return schemas.UserUpdate(
            username="Updater",
            password="test_password",
            email="updater@mail.com",
            first_name="Updater",
            last_name="test",
    )


@pytest.fixture
def user_in_patch() -> schemas.UserPatch:
    return schemas.UserPatch(
            email="patch@mail.com",
            first_name="Patcher",
            last_name="test",
    )


@pytest_asyncio.fixture
async def db_users_pass_not_encrypted(
        db_session,
        user_in,
        user_in_2
) -> MutableSequence[models.User]:
    db_users = []
    for user_to_db in (user_in, user_in_2):
        user_data = user_to_db.dict()
        password = user_data.pop("password")
        db_user = models.User(hashed_password=password, **user_data)
        db_session.add(db_user)
        await db_session.commit()
        await db_session.refresh(db_user)
        db_users.append(db_user)
    return db_users
