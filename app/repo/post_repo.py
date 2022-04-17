from typing import Optional, List, Union

from app.db.session import DBEngine
from app.models.schema.post_schema import Post, PostCreate
from app.repo.base_repo import BaseRepo
from app.repo.dao.post_dao import PostDao


class PostRepo(BaseRepo):
    def __init__(self, engine: DBEngine):
        super().__init__(engine)

    def get_latest_posts_by(self, route: str) -> List[Post]:
        posts = PostDao.get_latest_posts_by(self._db(), route)

        return [Post(**post._asdict()) for post in posts]

    def find_last(self) -> Optional[Post]:
        model = PostDao.find_last(self._db())
        return Post(**model._asdict()) if model else None

    def merge_all(self, posts: List[Post]):
        db = self._db()
        for post in posts:
            PostDao.merge(db, post)
        db.commit()

    def merge(self, post: Union[Post, PostCreate]):
        db = self._db()
        PostDao.merge(db, post)
        db.commit()
