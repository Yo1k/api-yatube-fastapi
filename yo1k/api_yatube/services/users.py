from typing import Type, Union, Any

from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from .crud import DefaultService
from .. import models
from .. import schemas
from .auth import AuthService


class UsersService(
        DefaultService[models.User, schemas.UserCreate, schemas.UserUpdate]
):
    async def get_many(
            self,
            model_type: Type[models.User],
            skip: int = 0,
            limit: int = 100,
    ) -> list[models.User]:
        result = await self.session.execute(
                select(model_type)
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
            model_type: Type[models.User],
            obj_in: schemas.UserCreate,
    ) -> models.User:
        obj_data = obj_in.dict()
        password = obj_data.pop("password")
        db_obj = model_type(
                hashed_password=AuthService.get_password_hash(password),
                **obj_data
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def _get(
            self,
            model_type: Type[models.User],
            obj_id: int,
    ) -> models.User:
        result = await self.session.execute(
                select(model_type)
                .filter(model_type.id == obj_id)
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
            model_type: Type[models.User],
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
                    AuthService.get_password_hash(password)
            )
        return await super()._update(
                model_type=model_type,
                obj_in=update_data,
                obj_id=obj_id,
                exclude_unset=exclude_unset
        )
