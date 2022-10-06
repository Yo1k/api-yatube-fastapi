from fastapi import APIRouter, Depends
from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.users import UsersService
from yo1k.api_yatube import models

router = APIRouter(
        prefix="/users",
        tags=["users"]
)


@router.get(
        "/",
        response_model=list[schemas.User]
)
def get_users(
        skip: int = 0,
        limit: int = 100,
        users_service: UsersService = Depends()
):
    return users_service.get_many(
            model_type=models.User,
            skip=skip,
            limit=limit
    )


@router.get(
        "/{user_id}",
        response_model=schemas.User
)
def get_user(
        user_id: int,
        users_service: UsersService = Depends()
):
    return users_service.get(
            model_type=models.User,
            obj_id=user_id
    )


@router.post(
        "/",
        response_model=schemas.User
)
def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends()
):
    return users_service.create(
            model_type=models.User,
            obj_in=user
    )


@router.put(
        "/{user_id}",
        response_model=schemas.User
)
def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        users_service: UsersService = Depends()
):
    return users_service.update(
            model_type=models.User,
            obj_in=user,
            obj_id=user_id
    )


@router.patch(
        "/{user_id}",
        response_model=schemas.User
)
def partial_update_user(
        user_id: int,
        user: schemas.UserPatch,
        users_service: UsersService = Depends()
):
    return users_service.partial_update(
            model_type=models.User,
            obj_in=user,
            obj_id=user_id
    )


@router.delete(
        "/{user_id}",
        response_model=schemas.User
)
def delete_user(
        user_id: int,
        users_service: UsersService = Depends()
):
    return users_service.delete(
            model_type=models.User,
            obj_id=user_id
    )
