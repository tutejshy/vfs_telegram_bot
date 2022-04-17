from sqlalchemy.orm import Session

from app.db.session import DBEngine


class BaseRepo:
    def __init__(self, engine: DBEngine):
        self.__engine = engine

    def _db(self) -> Session:
        return next(self.__engine.get_session())
