import pytest

from yo1k.api_yatube import schemas, models
from yo1k.api_yatube.services.users import UsersService


@pytest.fixture()
def user_in():
    return schemas.UserCreate(
            username="Tester",
            password="test_password"
    )


@pytest.fixture
def users_service(db_session):
    return UsersService(
            session=db_session
    )


def test_get_many():
    pass


@pytest.mark.asyncio
async def test_create_user(
        db,
        user_in,
        users_service
):
    await db.create_table()
    user_db = await users_service.create(
          model_type=models.User,
          obj_in=user_in
    )

    assert user_db.username == user_in.username
    assert user_db.id == 1

    await db.drop_table()
