from typing import List, Optional

from app.db.session import DBEngine
from app.models.schema.category_schema import Category
from app.models.schema.center_schema import Center
from app.repo.base_repo import BaseRepo
from app.repo.dao.category_dao import CategoryDao
from app.repo.dao.center_dao import CenterDao


class CategoryRepo(BaseRepo):
    def __init__(self, engine: DBEngine):
        super().__init__(engine)

    def get_number_of_categories(self, route: str, center: str, parent: Optional[str]) -> int:
        return CategoryDao.get_number_of_categories(self._db(), route, center, parent)

    def merge(self, route: str, items: List[Category]):
        if items:
            db = self._db()
            for category in items:
                CategoryDao.merge(db, route, category)
            db.commit()

    def fetch_root_categories_by(self, route: str, center: str) -> List[Category]:
        return [Category(**m._asdict()) for m in CategoryDao.fetch_by(self._db(), route, center)]

    def fetch_categories_by(self, route: str, center: str, parent: Optional[str]) -> List[Category]:
        return [Category(**m._asdict()) for m in CategoryDao.fetch_by(self._db(), route, center, parent)]

    def find_category_by(self, route: str, center: str, code: str, parent: Optional[str]) -> Optional[Category]:
        model = CategoryDao.find_by(self._db(), route, center, code, parent)
        return Category(**model._asdict()) if model else None

    def contains_categories(self, route: str, center: str, parent: Optional[str] = None) -> bool:
        return CategoryDao.contains_categories(self._db(), route, center, parent)
