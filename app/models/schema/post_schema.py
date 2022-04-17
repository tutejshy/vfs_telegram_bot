from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.models.domain.post_db import PostStatus


class Post(BaseModel):
    post_id: int
    route: Optional[str]
    message: Optional[str]

    status: PostStatus

    post_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    route: Optional[str]
    message: Optional[str]

    status: Optional[PostStatus]

    post_at: Optional[datetime]
    updated_at: Optional[datetime]
