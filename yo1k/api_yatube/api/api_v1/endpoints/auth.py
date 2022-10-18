from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.auth import AuthService

router = APIRouter(
        prefix="/auth",
        tags=["auth"]
)


@router.post(
        "/sign-in",
        response_model=schemas.Token
)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends()
):
    return await auth_service.authenticate_user(
            username=form_data.username,
            password=form_data.password
    )
