from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models.domain.base import LoginDB
from app.models.schema.login_schema import LoginMerge, Login


class LoginDao:
    @staticmethod
    def find_by_login(db: Session, login: str) -> Optional[LoginDB]:
        return db.query(LoginDB).filter(LoginDB.login == login).first()

    @staticmethod
    def fetch_all(db: Session) -> List[LoginDB]:
        return db.query(LoginDB).all()

    @staticmethod
    def get_logins_grouped_by_route(db: Session) -> List[LoginDB]:
        return db.query(LoginDB).group_by(LoginDB.route).all()

    @staticmethod
    def get_number_of_logins(db: Session) -> int:
        return db.query(LoginDB).count()

    @staticmethod
    def create(db: Session, login: LoginMerge) -> LoginDB:
        model = LoginDB()
        model.login = login.login
        model.pwd = login.pwd
        model.to = login.to
        model.route = login.route

        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, login: Union[LoginMerge, Login]) -> LoginDB:
        model = LoginDao.find_by_login(db, login.login) or LoginDao.create(db, login)
        model.pwd = login.pwd
        model.to = login.to
        model.route = login.route or model.route
        model.status = login.status or model.status

        model.token = login.token or model.token

        model.login_at = login.login_at or model.login_at
        model.http_code = login.http_code or model.http_code
        model.error_count = login.error_count or model.error_count

        return model

    @staticmethod
    def clear(db: Session):
        # db.delete(LoginDB)
        print("IMPL ALL DELETING IS HERE")
