from typing import Optional

from sqlalchemy.orm import Session

from app.models.domain.base import AccountDB


class AccountDao:

    @staticmethod
    def find_by_actor(db: Session, actor_id: str) -> Optional[AccountDB]:
        return db.query(AccountDB).filter(AccountDB.actor_id == actor_id).first()

    @staticmethod
    def create(db: Session, actor_id: str, is_active: bool = True) -> AccountDB:
        model = AccountDB()
        model.actor_id = actor_id
        model.is_active = is_active
        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, actor_id: str, is_active: bool = True) -> AccountDB:
        model = AccountDao.find_by_actor(db, actor_id) or AccountDao.create(db, actor_id, is_active)
        model.actor_id = actor_id
        model.is_active = is_active

        return model
