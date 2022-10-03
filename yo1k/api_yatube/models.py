from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
    ForeignKey
)
from sqlalchemy.orm import relationship

from yo1k.api_yatube.database import Base


class User(Base):
    __tablename__ = "users"

    first_name = Column(String(150))
    email = Column(String, nullable=True, unique=True)
    id = Column(Integer, index=True, primary_key=True)
    last_name = Column(String(150))
    hashed_password = Column(String)
    username = Column(String(150), index=True, unique=True)

    posts = relationship(
            "Post",
            back_populates="author",
            cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
                f"User("
                f"id={self.id}, "
                f"username={self.username}, "
                f"first_name={self.first_name}, "
                f"last_name={self.last_name}, "
                f"email={self.email}"
                f")"
        )


class Post(Base):
    __tablename__ = "posts"

    author_id = Column(Integer, ForeignKey("users.id"))
    # image = ...
    id = Column(Integer, index=True, primary_key=True)
    pub_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    text = Column(Text(), nullable=False)

    author = relationship(
            "User",
            back_populates="posts"
    )
    # group = relationship()

    def __repr__(self):
        return (
                f"Post("
                f"id={self.id}, "
                f"author_id={self.author_id}, "
                f"text={self.text[:15]}, "
                f"pub_date={self.pub_date}"
                f")"
        )
