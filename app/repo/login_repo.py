import threading
from typing import Optional, List

from app.db.session import DBEngine

from app.models.schema.login_schema import LoginMerge, Login, Route
from app.repo.base_repo import BaseRepo
from app.repo.dao.login_dao import LoginDao


class LoginRepo(BaseRepo):

    def __init__(self, engine: DBEngine):
        super().__init__(engine)
        self._cache: List[Login] = []

    def register_logins(self, items: List[LoginMerge]) -> bool:
        db = self._db()
        auths = [LoginDao.merge(db, a) for a in items]
        if auths:
            db.commit()
            lock = threading.Lock()
            lock.acquire()
            self._cache = [Login(**m._asdict()) for m in LoginDao.fetch_all(db)]
            lock.release()
            return True

        return False

    def has_logins(self) -> bool:
        if not self._cache:
            self._cache = [Login(**m._asdict()) for m in LoginDao.fetch_all(self._db())]

        return True if self._cache else False

    def get_available_routes(self) -> List[Route]:
        logins = LoginDao.get_logins_grouped_by_route(self._db())
        return [Route(route=login.route, to=login.to) for login in logins]

    def get_available_login(self) -> Optional[Login]:
        sorted_list = sorted(self._cache, key=lambda x: x.login_at, reverse=True)
        return sorted_list[0] if sorted_list else None

    def update_login(self, login: Login):
        db = self._db()
        LoginDao.merge(db, login)
        db.commit()

    # def is_available(self) -> bool:
    #     return False

    def get_number_of_logins(self) -> int:
        return LoginDao.get_number_of_logins(self._db())

    def clear(self):
        db = self._db()
        self._cache.clear()
        LoginDao.clear(db)
        db.commit()
