from fastapi import APIRouter, Depends
from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.users import UsersService
from yo1k.api_yatube.services.auth import AuthService, get_current_user
from yo1k.api_yatube import models

router = APIRouter(
        prefix="/users",
        tags=["users"]
)


@router.get(
        "/",
        response_model=list[schemas.User]
)
async def get_users(
        skip: int = 0,
        limit: int = 100,
        users_service: UsersService = Depends()
):
    return await users_service.get_many(
            skip=skip,
            limit=limit
    )


@router.get(
        "/me",
        response_model=schemas.User
)
async def get_user(
        current_user: schemas.User = Depends(get_current_user),
        users_service: UsersService = Depends()
):
    return await users_service.get(
            obj_id=current_user.id
    )


@router.get(
        "/{user_id}",
        response_model=schemas.User
)
async def get_user(
        user_id: int,
        users_service: UsersService = Depends()
):
    return await users_service.get(
            obj_id=user_id
    )


@router.post(
        "/",
        response_model=schemas.Token
)
async def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends()
):
    db_user = await users_service.create(
            obj_in=user
    )

    return AuthService.create_access_token(
            user=db_user
    )


@router.put(
        "/me",
        response_model=schemas.User
)
async def update_user(
        user: schemas.UserUpdate,
        current_user: schemas.User = Depends(get_current_user),
        users_service: UsersService = Depends()
):
    return await users_service.update(
            obj_in=user,
            obj_id=current_user.id
    )


@router.patch(
        "/me",
        response_model=schemas.User
)
async def partial_update_user(
        user: schemas.UserPatch,
        current_user: schemas.User = Depends(get_current_user),
        users_service: UsersService = Depends()
):
    return await users_service.partial_update(
            obj_in=user,
            obj_id=current_user.id
    )


@router.delete(
        "/me",
        response_model=schemas.User
)
async def delete_user(
        current_user: schemas.User = Depends(get_current_user),
        users_service: UsersService = Depends()
):
    return await users_service.delete(
            obj_id=current_user.id
    )
