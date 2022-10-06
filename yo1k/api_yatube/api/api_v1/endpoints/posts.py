from fastapi import APIRouter, Depends
from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.posts import PostsService
from yo1k.api_yatube import models


router = APIRouter(
        prefix="/posts",
        tags=["posts"]
)


@router.get(
        "/",
        response_model=list[schemas.Post]
)
def get_posts(
        skip: int = 0,
        limit: int = 10,
        posts_service: PostsService = Depends()
):
    return posts_service.get_many(
            model_type=models.Post,
            skip=skip,
            limit=limit
    )


@router.get(
        "/{post_id}",
        response_model=schemas.Post
)
def get_post(
        post_id: int,
        posts_service: PostsService = Depends()
):
    return posts_service.get(
            model_type=models.Post,
            obj_id=post_id
    )


@router.post(
        "/",
        response_model=schemas.Post
)
def create_post(
        post: schemas.PostCreate,
        posts_service: PostsService = Depends()
):
    return posts_service.create(
            model_type=models.Post,
            obj_in=post
    )


@router.put(
        "/{post_id}",
        response_model=schemas.Post
)
def update_post(
        post_id: int,
        post: schemas.PostUpdate,
        posts_service: PostsService = Depends()
):
    return posts_service.update(
            model_type=models.Post,
            obj_in=post,
            obj_id=post_id
    )


@router.patch(
        "/{post_id}",
        response_model=schemas.Post
)
def partial_update_post(
        post: schemas.PostPatch,
        post_id: int,
        posts_service: PostsService = Depends()
):
    return posts_service.partial_update(
            model_type=models.Post,
            obj_in=post,
            obj_id=post_id
    )


@router.delete(
        "/{post_id}",
        response_model=schemas.Post
)
def delete_post(
        post_id: int,
        posts_service: PostsService = Depends()
):
    return posts_service.delete(
            model_type=models.Post,
            obj_id=post_id
    )
