from app.db.session import DBEngine
from app.models.schema.account_schema import Account
from app.repo.base_repo import BaseRepo
from app.repo.dao.account_dao import AccountDao


class AccountRepo(BaseRepo):
    def __init__(self, engine: DBEngine):
        super().__init__(engine)

    def logged_in(self, actor_id: str) -> bool:
        account = AccountDao.find_by_actor(self._db(), actor_id)
        return account.is_active if account else False

    def auth(self, actor_id: str) -> Account:
        db = self._db()
        model = AccountDao.merge(db, actor_id)
        db.flush()
        db.commit()
        db.refresh(model)
        return Account(**model._asdict())
