from typing import Type, Union, Any

from .crud import DefaultService
from .. import models
from .. import schemas


class UsersService(
        DefaultService[models.User, schemas.UserCreate, schemas.UserUpdate]
):
    def create(
            self,
            model_type: Type[models.User],
            obj_in: schemas.UserCreate,
    ) -> models.User:
        obj_data = obj_in.dict()
        password = obj_data.pop("password")
        fake_hashed_password = password + "notreallyhashed"
        db_obj = model_type(
                hashed_password=fake_hashed_password,
                **obj_data
        )
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def _update(
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
            update_data["hashed_password"] = password + "notreallyhashed"
        return super()._update(
                model_type=model_type,
                obj_in=update_data,
                obj_id=obj_id,
                exclude_unset=exclude_unset
        )
