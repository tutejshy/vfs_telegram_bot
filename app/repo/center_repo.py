from typing import List, Optional

from app.db.session import DBEngine
from app.models.schema.center_schema import Center
from app.repo.base_repo import BaseRepo
from app.repo.dao.center_dao import CenterDao


class CenterRepo(BaseRepo):
    def __init__(self, engine: DBEngine):
        super().__init__(engine)

    def get_number_of_centers(self, route: str) -> int:
        return CenterDao.get_number_of_centers(self._db(), route)

    def merge(self, route: str, items: List[Center]):
        if items:
            db = self._db()
            for center in items:
                CenterDao.merge(db, route, center)
            db.commit()

    def fetch_centers_by(self, route: str) -> List[Center]:
        return [Center(**m._asdict()) for m in CenterDao.fetch_by_route(self._db(), route)]

    def find_center_by(self, route: str, code: str) -> Optional[Center]:
        model = CenterDao.find_by(self._db(), route, code)
        return Center(**model._asdict()) if model else None
