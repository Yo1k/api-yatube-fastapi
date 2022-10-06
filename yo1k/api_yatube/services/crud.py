from typing import TypeVar, Type, Generic, Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db, Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DefaultService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session: Session = Depends(get_db)):
        self.session: Session = session

    def get(
            self,
            model_type: Type[ModelType],
            obj_id: int,
    ) -> ModelType:
        return self._get(model_type, obj_id)

    def get_many(
            self,
            model_type: Type[ModelType],
            skip: int = 0,
            limit: int = 100,
    ) -> list[ModelType]:
        return (
                self.session
                .query(model_type)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def create(
            self,
            model_type: Type[ModelType],
            obj_in: CreateSchemaType,
    ) -> ModelType:
        db_obj = model_type(**obj_in.dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(
            self,
            model_type: Type[ModelType],
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int
    ) -> ModelType:
        return self._update(model_type, obj_in, obj_id, exclude_unset=False)

    def partial_update(
            self,
            model_type: Type[ModelType],
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int
    ) -> ModelType:
        return self._update(model_type, obj_in, obj_id, exclude_unset=True)

    def delete(
            self,
            model_type: Type[ModelType],
            obj_id: int
    ) -> ModelType:
        db_obj = self._get(model_type, obj_id)
        if not db_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj

    def _get(
            self,
            model_type: Type[ModelType],
            obj_id: int,
    ) -> ModelType:
        obj = (
                self.session
                .query(model_type)
                .filter(model_type.id == obj_id)
                .first()
        )
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return obj

    def _update(
            self,
            model_type: Type[ModelType],
            obj_in: Union[UpdateSchemaType, dict[str, Any]],
            obj_id: int,
            exclude_unset: bool
    ) -> ModelType:
        db_obj = self._get(model_type, obj_id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=exclude_unset)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
