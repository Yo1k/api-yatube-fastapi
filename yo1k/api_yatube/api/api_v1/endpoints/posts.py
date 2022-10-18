from fastapi import APIRouter, Depends
from yo1k.api_yatube import schemas
from yo1k.api_yatube.services.posts import PostsService
from yo1k.api_yatube import models
from yo1k.api_yatube.services.auth import get_current_user

router = APIRouter(
        prefix="/posts",
        tags=["posts"]
)


@router.get(
        "/",
        response_model=list[schemas.Post]
)
async def get_posts(
        skip: int = 0,
        limit: int = 10,
        posts_service: PostsService = Depends()
):
    return await posts_service.get_many(
            model_type=models.Post,
            skip=skip,
            limit=limit
    )


@router.get(
        "/{post_id}",
        response_model=schemas.Post
)
async def get_post(
        post_id: int,
        posts_service: PostsService = Depends()
):
    return await posts_service.get(
            model_type=models.Post,
            obj_id=post_id
    )


@router.post(
        "/",
        response_model=schemas.Post
)
async def create_post(
        post: schemas.PostCreate,
        current_user: schemas.User = Depends(get_current_user),
        posts_service: PostsService = Depends()
):
    return await posts_service.create_with_owner(
            model_type=models.Post,
            obj_in=post,
            owner_id=current_user.id
    )


@router.put(
        "/{post_id}",
        response_model=schemas.Post
)
async def update_post(
        post: schemas.PostUpdate,
        post_id: int,
        current_user: schemas.User = Depends(get_current_user),
        posts_service: PostsService = Depends()
):
    await posts_service.verify_authorization(
            model_type=models.Post,
            obj_id=post_id,
            owner_id=current_user.id
    )
    return await posts_service.update(
            model_type=models.Post,
            obj_in=post,
            obj_id=post_id
    )


@router.patch(
        "/{post_id}",
        response_model=schemas.Post
)
async def partial_update_post(
        post: schemas.PostPatch,
        post_id: int,
        current_user: schemas.User = Depends(get_current_user),
        posts_service: PostsService = Depends()
):
    await posts_service.verify_authorization(
            model_type=models.Post,
            obj_id=post_id,
            owner_id=current_user.id
    )
    return await posts_service.partial_update(
            model_type=models.Post,
            obj_in=post,
            obj_id=post_id
    )


@router.delete(
        "/{post_id}",
        response_model=schemas.Post
)
async def delete_post(
        post_id: int,
        current_user: schemas.User = Depends(get_current_user),
        posts_service: PostsService = Depends()
):
    await posts_service.verify_authorization(
            model_type=models.Post,
            obj_id=post_id,
            owner_id=current_user.id
    )
    return await posts_service.delete(
            model_type=models.Post,
            obj_id=post_id
    )
