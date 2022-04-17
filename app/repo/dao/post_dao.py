import datetime
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models.domain.post_db import PostDB, PostStatus
from app.models.schema.post_schema import PostCreate, Post


class PostDao:
    @staticmethod
    def find_by_id(db: Session, post_id: int) -> Optional[PostDB]:
        return db.query(PostDB).filter(PostDB.post_id == post_id).first()

    @staticmethod
    def get_latest_posts_by(db: Session, route: str) -> List[PostDB]:
        return db.query(PostDB).filter(PostDB.route == route, PostDB.status == PostStatus.CREATED).order_by(PostDB.created_at.desc()).all()

    @staticmethod
    def find_last(db: Session) -> Optional[PostDB]:
        return db.query(PostDB).order_by(PostDB.created_at.desc()).first()

    @staticmethod
    def create(db: Session, post: PostCreate) -> PostDB:
        model = PostDB()
        model.route = post.route
        model.message = post.message
        model.status = post.status

        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, post: Union[Post, PostCreate]) -> PostDB:
        if isinstance(post, Post):
            model = PostDao.find_by_id(db, post.post_id)
            if model:
                model.route = post.route
                model.message = post.message
                model.status = post.status

                model.updated_at = datetime.datetime.now()
                return model

        return PostDao.create(db, post)

    @staticmethod
    def clear(db: Session):
        print("IMPL ALL DELETING IS HERE")
