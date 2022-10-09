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
    pass


class PostUpdate(PostCreate):
    pass


class PostPatch(PostUpdate):
    author_id: Optional[int] = None
    text: Optional[str] = None
