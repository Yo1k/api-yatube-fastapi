import pytest

from yo1k.api_yatube import models
from yo1k.api_yatube.services.users import UsersService


@pytest.fixture
def users_service(db_session):
    return UsersService(
            session=db_session
    )


@pytest.mark.usefixtures('clear_tables')
@pytest.mark.asyncio
async def test_create_user(
        user_in,
        users_service
):
    user_db = await users_service.create(
          model_type=models.User,
          obj_in=user_in
    )

    assert user_db.username == user_in.username
    assert user_db.id == 1


@pytest.mark.asyncio
async def test_create_user_2(
        user_in,
        users_service
):
    user_db = await users_service.create(
          model_type=models.User,
          obj_in=user_in
    )

    assert user_db.username == user_in.username
    assert user_db.id == 1


if __name__ == "__main__":
    pytest.main()
