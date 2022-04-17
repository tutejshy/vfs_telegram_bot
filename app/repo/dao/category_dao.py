from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models.domain.category_db import CategoryDB
from app.models.schema.category_schema import Category


class CategoryDao:
    @staticmethod
    def find_by(db: Session, route: str, center: str, code: str, parent: Optional[str] = None) -> Optional[CategoryDB]:
        return db.query(CategoryDB).filter(CategoryDB.route == route,
                                           CategoryDB.center == center,
                                           CategoryDB.code == code,
                                           CategoryDB.parent == parent).first()

    @staticmethod
    def contains_categories(db: Session, route: str, center: str, parent: Optional[str] = None) -> bool:
        return db.query(CategoryDB).filter(CategoryDB.route == route,
                                           CategoryDB.center == center,
                                           CategoryDB.parent == parent).count() > 0

    @staticmethod
    def fetch_by(db: Session, route: str, center: str, parent: Optional[str] = None) -> List[CategoryDB]:
        return db.query(CategoryDB).filter(CategoryDB.route == route,
                                           CategoryDB.center == center,
                                           CategoryDB.parent == parent).all()

    @staticmethod
    def get_number_of_categories(db: Session, route: str, center: str, parent: Optional[str] = None) -> int:
        return db.query(CategoryDB).filter(CategoryDB.route == route,
                                           CategoryDB.center == center,
                                           CategoryDB.parent == parent).count()

    @staticmethod
    def create(db: Session, route: str, category: Category) -> CategoryDB:
        model = CategoryDB()
        model.route = route
        model.center = category.center
        model.name = category.name
        model.code = category.code
        model.parent = category.parent
        model.mission_code = category.mission_code

        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, route: str, category: Union[Category]) -> CategoryDB:
        model = CategoryDao.find_by(db, route, category.center, category.code, category.parent) or CategoryDao.create(db, route, category)

        model.center = category.center or model.center
        model.name = category.name or model.name
        model.code = category.code or model.code
        model.mission_code = category.mission_code or model.mission_code
        model.parent = category.parent or model.parent

        return model
