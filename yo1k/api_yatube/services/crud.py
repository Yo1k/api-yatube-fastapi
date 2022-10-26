from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from yo1k.api_yatube.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDService(ABC, Generic[ModelType, CreateSchemaType,
                               UpdateSchemaType]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session: AsyncSession = session

    @property
    @abstractmethod
    def model_type(self) -> Type[ModelType]:
        pass

    async def get(
            self,
            obj_id: int,
    ) -> ModelType:
        return await self._get(obj_id)

    async def get_many(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> list[ModelType]:
        result = await self.session.execute(
                select(self.model_type)
                .offset(skip)
                .limit(limit)
        )
        return result.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
    ) -> ModelType:
        db_obj = self.model_type(**obj_in.dict())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int
    ) -> ModelType:
        return await self._update(
                obj_in,
                obj_id,
                exclude_unset=False
        )

    async def partial_update(
            self,
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int
    ) -> ModelType:
        return await self._update(
                obj_in,
                obj_id,
                exclude_unset=True
        )

    async def delete(
            self,
            obj_id: int
    ) -> ModelType:
        db_obj = await self._get(obj_id)
        if not db_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        await self.session.delete(db_obj)
        await self.session.commit()
        return db_obj

    async def verify_authorization(
            self,
            obj_id: int,
            owner_id: int
    ) -> None:
        raise NotImplementedError

    async def _get(
            self,
            obj_id: int,
    ) -> ModelType:
        result = await self.session.execute(
                select(self.model_type)
                .filter(self.model_type.id == obj_id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return obj

    async def _update(
            self,
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int,
            exclude_unset: bool
    ) -> ModelType:
        db_obj = await self._get(obj_id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=exclude_unset)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
