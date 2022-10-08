from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.auth import AuthService, get_current_user

router = APIRouter(
        prefix="/auth",
        tags=["auth"]
)


@router.get(
        "/me",
        response_model=schemas.User
)
def get_current_user(
        user: schemas.User = Depends(get_current_user)
):
    return user


@router.post(
        "/sign-in",
        response_model=schemas.Token
)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends()
):
    return auth_service.authenticate_user(
            username=form_data.username,
            password=form_data.password
    )


@router.post(
        "/sign-up",
        response_model=schemas.Token
)
def sign_up(
        user: schemas.UserCreate,
        auth_service: AuthService = Depends()
):
    return auth_service.register_new_user(
            user_in=user
    )
