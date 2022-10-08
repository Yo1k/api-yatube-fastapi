from fastapi import APIRouter
from .endpoints import auth, posts, users

router = APIRouter(
        prefix="/api/v1",
        tags=["api_v1"]
)

router.include_router(auth.router)
router.include_router(posts.router)
router.include_router(users.router)
