from collections.abc import Callable
from typing import Type, Union, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import joinedload

from .crud import CRUDService
from .. import models
from .. import schemas
from .auth import AuthService
from ..database import get_async_session


class UsersService(
        CRUDService[models.User, schemas.UserCreate, schemas.UserUpdate]
):
    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session),
            hash_pass_func: Optional[Callable[[str], str]] = None

    ):
        super().__init__(session=session)
        self.hash_pass_func = (
                AuthService.get_password_hash if hash_pass_func is None
                else hash_pass_func
        )

    @property
    def model_type(self) -> Type[models.User]:
        return models.User

    async def get_many(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> list[models.User]:
        result = await self.session.execute(
                select(self.model_type)
                .offset(skip)
                .limit(limit)
                .options(
                        joinedload(models.User.posts)
                        .load_only(models.Post.id)
                )
        )
        return result.scalars().unique().all()

    async def create(
            self,
            obj_in: schemas.UserCreate,
    ) -> models.User:
        obj_data = obj_in.dict()
        password = obj_data.pop("password")
        db_obj = self.model_type(
                hashed_password=self._get_password_hash(password),
                **obj_data
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def _get(
            self,
            obj_id: int,
    ) -> models.User:
        result = await self.session.execute(
                select(self.model_type)
                .filter(self.model_type.id == obj_id)
                .options(
                        joinedload(models.User.posts)
                        .load_only(models.Post.id)
                )
        )
        obj = result.scalars().unique().first()
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return obj

    async def _update(
            self,
            obj_in: Union[schemas.UserUpdate, dict[str, Any]],
            obj_id: int,
            exclude_unset: bool
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=exclude_unset)
        password = update_data.pop("password", None)
        if password:
            update_data["hashed_password"] = (
                    self._get_password_hash(password)
            )
        return await super()._update(
                obj_in=update_data,
                obj_id=obj_id,
                exclude_unset=exclude_unset
        )

    def _get_password_hash(self, password: str) -> str:
        return self.hash_pass_func(password)
