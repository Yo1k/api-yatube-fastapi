from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from yo1k.api_yatube.database import get_db
from yo1k.api_yatube import schemas, crud

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
        )


@app.get("/users/", response_model=list[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_users(db, skip, limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
        user_id: int,
        user_in: schemas.UserUpdate,
        db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )
    return crud.update_user(db, db_obj=db_user, obj_in=user_in, partial=False)


@app.patch("/users/{user_id}", response_model=schemas.User)
def partial_update_user(
        user_id: int,
        user_in: schemas.UserPatch,
        db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )
    return crud.update_user(db, db_obj=db_user, obj_in=user_in, partial=True)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )
    return crud.remove_user(db=db, user_id=user_id)


@app.post("/posts/", response_model=schemas.Post)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db)
):
    return crud.create_post(db, post=post)


@app.get("/posts/", response_model=list[schemas.Post])
def get_posts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_posts(db, skip, limit)


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id=post_id)


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(
        post_id: int,
        post_in: schemas.PostUpdate,
        db: Session = Depends(get_db)
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
        )
    return crud.update_post(
            db,
            post_obj=db_post,
            post_in=post_in,
            partial=False
    )


@app.patch("/posts/{post_id}", response_model=schemas.Post)
def partial_update_post(
        post_id: int,
        post_in: schemas.PostPatch,
        db: Session = Depends(get_db)
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
        )
    return crud.update_post(
            db,
            post_obj=db_post,
            post_in=post_in,
            partial=True
    )


@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
        )
    return crud.remove_post(db, post_id)
