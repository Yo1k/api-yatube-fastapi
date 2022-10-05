from typing import Any, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from yo1k.api_yatube.database import Base
from yo1k.api_yatube import models
from yo1k.api_yatube import schemas


def update_(
        db: Session,
        db_obj: Base,
        obj_in: Union[schemas.UserUpdate, dict[str, Any]],
        partial: bool,
) -> Base:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        if partial:
            exclude_unset = True
        else:
            exclude_unset = False
        update_data = obj_in.dict(exclude_unset=exclude_unset)

    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip=0, limit=100):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user_dict = user.dict()
    password = user_dict.pop("password")
    fake_hashed_password = password + "notreallyhashed"
    db_user = models.User(
            hashed_password=fake_hashed_password,
            **user_dict
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(
        db: Session,
        user_id: int
) -> Base:
    db_user = db.query(models.User).get(user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(
        db: Session,
        db_obj: Base,
        obj_in: schemas.UserUpdate,
        partial: bool,
) -> Base:
    if partial:
        exclude_unset = True
    else:
        exclude_unset = False
    user_dict = obj_in.dict(exclude_unset=exclude_unset)

    password = user_dict.pop("password", None)
    if password:
        fake_hashed_password = password + "notreallyhashed"
        user_dict["hashed_password"] = fake_hashed_password

    return update_(db, db_obj, obj_in=user_dict, partial=partial)


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    db_post = db.query(models.Post).offset(skip).limit(limit).all()
    print(f"db_post:{db_post}")
    return db_post


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(
        db: Session,
        post_obj: models.Post,
        post_in: Union[schemas.PostUpdate, dict[str, Any]],
        partial: bool,
) -> Base:
    return update_(db, db_obj=post_obj, obj_in=post_in, partial=partial)


def remove_post(db: Session, post_id: int):
    db_post = db.query(models.Post).get(post_id)
    db.delete(db_post)
    db.commit()
    return db_post
