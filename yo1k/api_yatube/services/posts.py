from .crud import DefaultService
from .. import models
from .. import schemas


class PostsService(
        DefaultService[models.Post, schemas.PostCreate, schemas.PostUpdate]
):
    pass
