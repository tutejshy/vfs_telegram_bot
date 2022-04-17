import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, Enum

from app.models.domain.base_db import BaseDB


class PostStatus(enum.Enum):
    CREATED = 'created'
    POSTED = 'posted'


class PostDB(BaseDB):
    post_id = Column(Integer, primary_key=True, unique=True, index=True)
    route = Column(String(56),  index=True)
    message = Column(String(256))
    status = Column(Enum(PostStatus), default=PostStatus.CREATED)

    post_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now)
