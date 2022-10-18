from typing import Optional

from pydantic import BaseModel

from .post import PostID


class UserBase(BaseModel):
    first_name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None
    username: str


class User(UserBase):
    id: int
    posts: list[PostID] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserPatch(UserUpdate):
    password: Optional[str] = None
    username: Optional[str] = None
