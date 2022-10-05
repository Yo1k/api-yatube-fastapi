from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    text: str


class Post(PostBase):
    author_id: int
    id: int
    pub_date: datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    author_id: int


class PostUpdate(PostCreate):
    pass


class PostPatch(PostUpdate):
    author_id: Optional[int] = None
    text: Optional[str] = None


class UserBase(BaseModel):
    first_name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None
    username: str


class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserPatch(UserUpdate):
    password: Optional[str] = None
    username: Optional[str] = None
