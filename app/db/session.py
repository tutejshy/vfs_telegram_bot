from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.domain.base import BaseDB


class DBEngine:
    def __init__(self, database_uri: str):
        self.engine = create_engine(database_uri, echo=True)
        self.session = sessionmaker(self.engine)
        BaseDB.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator:
        with self.session() as s:
            yield s
