from datetime import datetime
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models.domain.base import CheatActionDB
from app.models.domain.center_db import CenterDB
from app.models.schema.center_schema import Center


class CenterDao:

    @staticmethod
    def find_by(db: Session, route: str, code: str) -> Optional[CenterDB]:
        return db.query(CenterDB).filter(CenterDB.route == route, CenterDB.code == code).first()

    @staticmethod
    def fetch_by_route(db: Session, route: str) -> List[CenterDB]:
        return db.query(CenterDB).filter(CenterDB.route == route).all()

    @staticmethod
    def get_number_of_centers(db: Session, route: str) -> int:
        return db.query(CenterDB).filter(CenterDB.route == route).count()

    @staticmethod
    def create(db: Session, route: str, center: Center) -> CenterDB:
        model = CenterDB()
        model.route = route
        model.name = center.name
        model.code = center.code

        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, route: str, center: Union[Center]) -> CenterDB:
        model = CenterDao.find_by(db, route, center.code) or CenterDao.create(db, route, center)
        model.name = center.name
        model.code = center.code or model.code

        return model
