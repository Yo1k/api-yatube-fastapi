from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..database import get_async_session
from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/sign-in")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    return AuthService.verify_token(token)


class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
            user: models.User,
            expires_delta: Optional[timedelta] = None,
    ) -> schemas.Token:
        user_data = jsonable_encoder(user)
        if not expires_delta:
            expires_delta = timedelta(
                    minutes=settings.access_token_expire_minutes
            )
        now = datetime.utcnow()
        payload = {
                "iat": now,
                "nbf": now,
                "exp": now + expires_delta,
                "sub": str(user.id),
                "user": schemas.User(**user_data).dict()
        }
        token = jwt.encode(
                payload,
                key=settings.secret_key,
                algorithm=settings.algorithm
        )
        return schemas.Token(access_token=token)

    @staticmethod
    def verify_password(
            plain_password: str,
            hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_token(token: str) -> schemas.User:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(
                    token,
                    key=settings.secret_key,
                    algorithms=settings.algorithm
            )
        except JWTError:
            raise exception from None
        user_data = payload.get("user")
        try:
            user = schemas.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session: AsyncSession = session

    async def authenticate_user(
            self,
            username: str,
            password: str,
    ) -> schemas.Token:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
        )
        result = await self.session.execute(
                select(models.User)
                .filter(models.User.username == username)
        )
        user: models.User = result.scalars().first()

        if not user:
            raise exception

        if not self.verify_password(
                plain_password=password,
                hashed_password=user.hashed_password
        ):
            raise exception

        return self.create_access_token(user)
