from collections.abc import MutableSequence, KeysView

import pytest
from sqlalchemy.future import select

from yo1k.api_yatube import models, schemas
from yo1k.api_yatube.services.users import UsersService
from fastapi import HTTPException, status


@pytest.fixture
def users_service(
        db_session,
        plain_hash_pass,
) -> UsersService:
    return UsersService(
            session=db_session,
            hash_pass_func=plain_hash_pass
    )


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


@pytest.mark.parametrize(
        "fixt_user_in",
        [
                "user_in_update_all_attrs",
                "user_in_update_partial_attrs"
        ]
)
@pytest.mark.asyncio
async def test__update_user_include_unset(
        db_users_pass_not_encrypted: MutableSequence[models.User],
        users_service: UsersService,
        fixt_user_in: str,
        request,
        schemas_user_update_field_names: KeysView,
) -> None:
    num_db_users = len(db_users_pass_not_encrypted)
    user_in: schemas.UserUpdate = request.getfixturevalue(fixt_user_in)
    last_db_user = db_users_pass_not_encrypted[-1]
    updated_db_user = await users_service._update(
            model_type=models.User,
            obj_in=user_in,
            obj_id=last_db_user.id,
            exclude_unset=False,
    )
    result = await users_service.session.execute(select(models.User))
    num_updated_db_users = len(result.scalars().all())

    assert num_db_users == num_updated_db_users

    # checks that all `user_in` fields are saved to DB
    for field_name in schemas_user_update_field_names:
        if field_name == "password":
            assert updated_db_user.hashed_password == user_in.password
        else:
            assert getattr(updated_db_user, field_name) \
                    == getattr(user_in, field_name)


@pytest.mark.parametrize(
        "fixt_user_in",
        [
                "user_in_patch_partial_attrs",
                "user_in_patch_all_attrs"
        ]
)
@pytest.mark.asyncio
async def test__update_user_exclude_unset(
        db_users_pass_not_encrypted: MutableSequence[models.User],
        users_service: UsersService,
        fixt_user_in: str,
        schemas_user_patch_field_names: KeysView,
        request,
) -> None:
    num_db_users = len(db_users_pass_not_encrypted)
    user_in: schemas.UserPatch = request.getfixturevalue(fixt_user_in)
    last_db_user = db_users_pass_not_encrypted[-1]
    updated_db_user = await users_service._update(
            model_type=models.User,
            obj_in=user_in,
            obj_id=last_db_user.id,
            exclude_unset=True,
    )
    fields_set = user_in.__fields_set__
    result = await users_service.session.execute(select(models.User))
    num_updated_db_users = len(result.scalars().all())

    assert num_db_users == num_updated_db_users

    # checks that included `user_in` fields are saved to DB
    for field_name in fields_set:
        if field_name == "password":
            assert updated_db_user.hashed_password \
                    == user_in.password
        else:
            assert getattr(updated_db_user, field_name) \
                    == getattr(user_in, field_name)

    # checks that excluded `user_in` fields are not saved to DB
    excluded_fields = set(schemas_user_patch_field_names) - fields_set
    for field_name in excluded_fields:
        if field_name == "password":
            assert last_db_user.hashed_password \
                    == updated_db_user.hashed_password
        else:
            assert getattr(last_db_user, field_name) \
                    == getattr(updated_db_user, field_name)


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


@pytest.mark.asyncio  # SKTODO remove useless test
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
