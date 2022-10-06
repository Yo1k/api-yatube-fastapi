from fastapi import APIRouter
from .endpoints import posts, users

router = APIRouter(
        prefix="/api/v1",
        tags=["api_v1"]
)

router.include_router(posts.router)
router.include_router(users.router)

