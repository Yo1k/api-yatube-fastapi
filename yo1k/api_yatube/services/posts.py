from typing import Type

from fastapi import HTTPException, status

from .crud import DefaultService
from .. import models
from .. import schemas


class PostsService(
        DefaultService[models.Post, schemas.PostCreate, schemas.PostUpdate]
):
    async def create_with_owner(
            self,
            model_type: Type[models.Post],
            obj_in: schemas.PostCreate,
            owner_id: int,
    ) -> models.Post:
        db_obj = model_type(
                author_id=owner_id,
                **obj_in.dict()
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def verify_authorization(
            self,
            model_type,
            obj_id: int,
            owner_id: int
    ) -> None:
        exception = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
        )
        db_obj = await self.get(model_type, obj_id)
        if db_obj.author_id != owner_id:
            raise exception
