from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.domain.base import CheatActionDB


class CheatActionDao:
    @staticmethod
    def fetch_all(db: Session) -> List[CheatActionDB]:
        return db.query(CheatActionDB).all()

    @staticmethod
    def create(db: Session, actor_id: str, action: Optional[str], cheat_at: datetime = datetime.now()) -> CheatActionDB:
        model = CheatActionDB()
        model.actor_id = actor_id
        model.action = action
        model.cheat_at = cheat_at

        db.add(model)

        return model
