from collections.abc import MutableSequence

import pytest

from yo1k.api_yatube import models, schemas
from yo1k.api_yatube.services.users import UsersService
from fastapi import HTTPException, status


@pytest.fixture
def users_service(db_session) -> UsersService:
    return UsersService(
            session=db_session
    )


@pytest.mark.usefixtures("clear_tables")
@pytest.mark.asyncio
async def test__get_existed_user(
        users_service: UsersService,
        db_users_pass_not_encrypted: MutableSequence[models.User]
) -> None:
    first_db_user = db_users_pass_not_encrypted[0]
    db_user = await users_service._get(
            model_type=models.User,
            obj_id=first_db_user.id
    )
    assert isinstance(db_user, models.User)
    assert db_user.username == first_db_user.username


@pytest.mark.usefixtures("clear_tables")
@pytest.mark.asyncio
async def test__get_non_existed_user(
        users_service: UsersService,
        db_users_pass_not_encrypted: MutableSequence[models.User]
) -> None:
    last_db_user = db_users_pass_not_encrypted[-1]
    with pytest.raises(HTTPException) as exp_info:
        await users_service._get(
                model_type=models.User,
                obj_id=last_db_user.id + 1,
        )
    assert exp_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("clear_tables")
@pytest.mark.asyncio
async def test__update_user_include_unset(
        db_users_pass_not_encrypted: MutableSequence[models.User],
        users_service: UsersService,
        user_in_update_all_attrs: schemas.UserUpdate,
) -> None:
    last_db_user = db_users_pass_not_encrypted[-1]
    updated_db_user = await users_service._update(
            model_type=models.User,
            obj_in=user_in_update_all_attrs,
            obj_id=last_db_user.id,
            exclude_unset=False,
    )
    assert updated_db_user.username == user_in_update_all_attrs.username


@pytest.mark.usefixtures('clear_tables')
@pytest.mark.asyncio
async def test_create_user(
        user_in: schemas.UserCreate,
        users_service: UsersService
) -> None:
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
