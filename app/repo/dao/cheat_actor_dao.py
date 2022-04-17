from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.domain.base import CheatActorDB


class CheatActorDao:
    @staticmethod
    def find_by_actor(db: Session, actor_id: str) -> Optional[CheatActorDB]:
        return db.query(CheatActorDB).filter(CheatActorDB.actor_id == actor_id).first()

    @staticmethod
    def fetch_all(db: Session) -> List[CheatActorDB]:
        return db.query(CheatActorDB).all()

    @staticmethod
    def create(db: Session, actor_id: str, cheat_count: int, last_cheat_at: datetime) -> CheatActorDB:
        model = CheatActorDB()
        model.actor_id = actor_id
        model.cheat_count = cheat_count
        model.last_cheat_at = last_cheat_at

        db.add(model)

        return model

    @staticmethod
    def merge(db: Session, actor_id: str, cheat_count: Optional[int], last_cheat_at: Optional[datetime]) -> CheatActorDB:
        model = CheatActorDao.find_by_actor(db, actor_id) or \
                CheatActorDao.create(db, actor_id, cheat_count or 0, last_cheat_at or datetime.now())

        model.cheat_count = cheat_count or model.cheat_count
        model.last_cheat_at = last_cheat_at or model.last_cheat_at

        return model
